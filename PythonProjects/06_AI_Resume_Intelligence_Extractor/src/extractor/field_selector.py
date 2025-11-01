"""
Utility to dynamically select which fields to extract.
Supports CLI-based filtering or full extraction.
"""

from extractor.fields import (
    ResumeNameField, ResumeEmailField, ResumePhoneField, ResumeLocationField,
    ResumeSkillsField, ResumeJobTitleField, ResumeCompanyField,
    ResumeExperienceField, ResumeTechStackField, ResumeScoreField
)

# Registry of all available field extractors
FIELD_REGISTRY = {
    "name": ResumeNameField,
    "email": ResumeEmailField,
    "phone": ResumePhoneField,
    "location": ResumeLocationField,
    "skills": ResumeSkillsField,
    "job_titles": ResumeJobTitleField,
    "companies": ResumeCompanyField,
    "experience": ResumeExperienceField,
    "tech_stack": ResumeTechStackField,
    "score": ResumeScoreField,
}

def get_selected_fields(selected=None):
    """
    Filters field registry based on user selection.
    
    Args:
        selected (list[str]): List of field names to extract.
    
    Returns:
        dict: Filtered field_name → class mapping.
    """
    if not selected:
        return FIELD_REGISTRY
    return {k: v for k, v in FIELD_REGISTRY.items() if k in selected}

