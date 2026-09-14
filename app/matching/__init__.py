"""Matching and entity resolution module"""
from app.matching.phone_matcher import PhoneMatcher
from app.matching.person_matcher import PersonMatcher
from app.matching.company_matcher import CompanyMatcher
from app.matching.resolver import EntityResolver

__all__ = ["PhoneMatcher", "PersonMatcher", "CompanyMatcher", "EntityResolver"]
