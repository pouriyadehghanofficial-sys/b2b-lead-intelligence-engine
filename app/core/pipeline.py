"""Core pipeline orchestration"""

import logging
from typing import List, Optional, Dict
from datetime import datetime
import json
import os
from app.search.router import SearchRouter
from app.extraction.phone import PhoneExtractor
from app.extraction.company import CompanyExtractor
from app.extraction.person import PersonExtractor
from app.validation.phone_validator import IranianPhoneValidator
from app.validation.industry_validator import IndustryValidator
from app.matching.resolver import EntityResolver
from app.scoring.confidence import ConfidenceEngine
from app.scoring.lead_score import LeadScorer
from app.scoring.freshness import FreshnessAnalyzer
from app.entities.lead import Lead, LeadStatus
from app.entities.evidence import Evidence, EvidenceType
from app.storage.db import Database
from app.network.client import HTTPClient
from app.query_generator import QueryGenerator
from app.llm.router import LLMRouter

logger = logging.getLogger(__name__)


class LeadDiscoveryPipeline:
    """Main pipeline for lead discovery and validation"""
    
    def __init__(self, db_path: str = "./data/leads.db"):
        self.db = Database(db_path)
        self.search_router = SearchRouter()
        self.phone_extractor = PhoneExtractor()
        self.company_extractor = CompanyExtractor()
        self.person_extractor = PersonExtractor()
        self.phone_validator = IranianPhoneValidator()
        self.industry_validator = IndustryValidator()
        self.entity_resolver = EntityResolver()
        self.confidence_engine = ConfidenceEngine()
        self.lead_scorer = LeadScorer()
        self.freshness_analyzer = FreshnessAnalyzer()
        self.llm_router = LLMRouter()
        self.query_generator = QueryGenerator(self.llm_router)
        self.http_client = HTTPClient()
        
        # Statistics
        self.stats = {
            'companies_found': 0,
            'people_found': 0,
            'phones_found': 0,
            'sources_checked': 0,
            'duplicates_removed': 0,
            'errors': 0,
        }
    
    def discover(
        self,
        industry: str,
        location: str,
        product: str = None,
        target_roles: List[str] = None,
        quantity: int = 100,
        max_queries: int = 20,
    ) -> List[Lead]:
        """Discover leads for given criteria"""
        logger.info(f"Starting lead discovery: {industry} in {location}")
        
        # Step 1: Generate queries
        logger.info("Step 1: Generating search queries...")
        queries = self.query_generator.generate(
            industry=industry,
            location=location,
            product=product,
            target_roles=target_roles,
            count=max_queries,
        )
        logger.info(f"Generated {len(queries)} queries")
        
        # Step 2: Search
        logger.info("Step 2: Searching sources...")
        search_results = []
        for query in queries:
            try:
                results = self.search_router.search(query, limit=10)
                search_results.extend(results)
                self.stats['sources_checked'] += 1
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {str(e)}")
                self.stats['errors'] += 1
        
        logger.info(f"Found {len(search_results)} search results")
        
        # Step 3: Extract and process
        logger.info("Step 3: Extracting companies, people, and contacts...")
        leads: Dict[str, Lead] = {}  # company_name -> Lead
        
        for result in search_results:
            try:
                # Extract content (simplified - would fetch full page in production)
                self._process_search_result(
                    result,
                    leads,
                    target_roles=target_roles,
                )
            except Exception as e:
                logger.warning(f"Processing failed for {result.url}: {str(e)}")
                self.stats['errors'] += 1
        
        # Step 4: Deduplication
        logger.info("Step 4: Deduplicating leads...")
        deduped_leads = self._deduplicate_leads(list(leads.values()))
        logger.info(f"Leads after deduplication: {len(deduped_leads)}")
        
        # Step 5: Scoring and filtering
        logger.info("Step 5: Scoring and ranking leads...")
        scored_leads = self.lead_scorer.batch_score(deduped_leads)
        
        # Filter by quantity
        final_leads = scored_leads[:quantity]
        
        logger.info(f"Lead discovery complete. Found {len(final_leads)} qualified leads.")
        return final_leads
    
    def _process_search_result(self, result, leads_dict, target_roles=None):
        """Process a single search result"""
        # Extract companies
        company_names = self.company_extractor.extract(result.snippet)
        
        for company_name in company_names[:1]:  # Take best company
            # Extract people and roles
            people = self.person_extractor.extract_person_mentions(result.snippet)
            
            # Extract phones
            phones = self.phone_extractor.extract(result.snippet)
            
            # Create or update lead
            if company_name not in leads_dict:
                lead = Lead(company_name=company_name)
                leads_dict[company_name] = lead
            else:
                lead = leads_dict[company_name]
            
            # Add person if found
            if people:
                person = people[0]  # Best match
                if not lead.person_name:
                    lead.person_name = person['name']
                    lead.role = person['role']
            
            # Add phone if found
            if phones and not lead.phone:
                lead.phone = phones[0]
            
            # Add evidence
            evidence = Evidence(
                url=result.url,
                source_type=EvidenceType.SEARCH_RESULT,
                extracted_text=result.snippet[:300],
                entity_type='company',
                entity_value=company_name,
                confidence=0.7,
            )
            lead.add_evidence(evidence)
            
            self.stats['companies_found'] += 1
    
    def _deduplicate_leads(self, leads: List[Lead]) -> List[Lead]:
        """Remove duplicate leads"""
        unique_leads = {}
        removed = 0
        
        for lead in leads:
            key = f"{lead.company_name}_{lead.person_name or ''}_{lead.phone or ''}"
            
            if key in unique_leads:
                # Merge with existing
                existing = unique_leads[key]
                existing = self.entity_resolver.merge_leads(existing, lead)
                unique_leads[key] = existing
                removed += 1
            else:
                unique_leads[key] = lead
        
        self.stats['duplicates_removed'] = removed
        return list(unique_leads.values())
