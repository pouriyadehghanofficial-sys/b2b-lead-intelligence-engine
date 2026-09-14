"""Query generation module"""

import logging
from typing import List
from app.llm.router import LLMRouter

logger = logging.getLogger(__name__)


class QueryGenerator:
    """Generate search queries from user input"""
    
    def __init__(self, llm_router: LLMRouter = None):
        self.llm_router = llm_router or LLMRouter()
    
    def generate(
        self,
        industry: str,
        location: str,
        product: str = None,
        target_roles: List[str] = None,
        count: int = 15,
    ) -> List[str]:
        """Generate diverse search queries"""
        queries = []
        
        # Persian-based queries
        queries.extend(self._generate_persian_queries(
            industry, location, product, target_roles
        ))
        
        # English-based queries
        queries.extend(self._generate_english_queries(
            industry, location, product, target_roles
        ))
        
        # AI-generated queries (if LLM available)
        if self.llm_router.is_available():
            ai_queries = self._generate_ai_queries(
                industry, location, product, target_roles, count=5
            )
            queries.extend(ai_queries)
        
        # Deduplicate and limit
        unique_queries = list(dict.fromkeys(queries))
        return unique_queries[:count]
    
    def _generate_persian_queries(self, industry, location, product, target_roles):
        """Generate Persian queries"""
        queries = []
        
        # Basic queries
        queries.append(f"{industry} {location}")
        queries.append(f"کارخانه {industry} {location}")
        queries.append(f"شرکت {industry} {location}")
        queries.append(f"تولیدکننده {industry} {location}")
        queries.append(f"نمایندگی {industry} {location}")
        
        # Contact queries
        queries.append(f"شماره تماس {industry} {location}")
        queries.append(f"تلفن {industry} {location}")
        queries.append(f"پیوند تماس {industry} {location}")
        
        # Role-based queries
        if target_roles:
            for role in target_roles[:3]:  # Top 3 roles
                queries.append(f"{role} {industry} {location}")
        
        # Product-based
        if product:
            queries.append(f"{product} {location}")
            queries.append(f"فروش {product} {location}")
            queries.append(f"خرید {product} {location}")
        
        # Directory/Business queries
        queries.append(f"فهرست {industry} {location}")
        queries.append(f"دایرکتوری {industry} {location}")
        queries.append(f"سایت {industry} {location}")
        
        return queries
    
    def _generate_english_queries(self, industry, location, product, target_roles):
        """Generate English queries"""
        queries = []
        
        # Basic
        queries.append(f"{industry} {location}")
        queries.append(f"{industry} manufacturers {location}")
        queries.append(f"{industry} companies {location}")
        
        # Contact
        queries.append(f"{industry} {location} contact")
        queries.append(f"{industry} {location} phone")
        
        # Product
        if product:
            queries.append(f"{product} suppliers {location}")
            queries.append(f"{product} dealers {location}")
        
        # B2B
        queries.append(f"{industry} b2b {location}")
        queries.append(f"{industry} wholesale {location}")
        
        return queries
    
    def _generate_ai_queries(self, industry, location, product, target_roles, count=5):
        """Generate queries using LLM"""
        if not self.llm_router.is_available():
            return []
        
        prompt = f"""
Generate {count} diverse and specific search queries to find B2B leads in the {industry} industry in {location}.
Focus on:
- Company names and variations
- Phone/contact information searches
- Role-based searches (for {', '.join(target_roles) if target_roles else 'business managers'})
- Directory and business listing queries
- Local language and transliterations

Return only the queries, one per line, without numbering.
"""
        
        try:
            response = self.llm_router.generate(
                prompt,
                temperature=0.5,
                max_tokens=500,
            )
            
            if response:
                return [q.strip() for q in response.split('\n') if q.strip()]
        except Exception as e:
            logger.warning(f"AI query generation failed: {str(e)}")
        
        return []
