import json
from typing import List, Dict

class FilterEngine:
    def __init__(self, profile, roadmap):
        """
        profile: instancia de ProgrammerProfile
        roadmap: instancia de StudyRoadmap
        """
        self.profile = profile
        self.roadmap = roadmap
        self.negative_keywords = ["senior", "expert", "5+ years", "team lead"]

    def apply_filters(self, jobs: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Clasifica trabajos en:
        - 'relevant_jobs': encajan con perfil actual
        - 'future_opportunities': requieren skills del roadmap
        """
        relevant, future = [], []
        for job in jobs:
            if self._is_relevant(job):
                relevant.append(job)
            elif self._is_future_opportunity(job):
                future.append(job)
        return {
            "relevant_jobs": relevant,
            "future_opportunities": future
        }

    def _is_relevant(self, job: Dict) -> bool:
        return (
            self._matches_skills(job, self.profile.get_skills()) and
            self._matches_experience(job) and
            not self._has_negative_keywords(job)
        )

    def _is_future_opportunity(self, job: Dict) -> bool:
        roadmap_skills = set(skill.lower() for skill in self.roadmap.get_skills())
        profile_skills = set(skill.lower() for skill in self.profile.get_skills())
        job_words = set(word.lower() for word in job.get("description", "").split())

        required = roadmap_skills & job_words
        already_have = profile_skills & job_words

        return bool(required - already_have)

    def _matches_skills(self, job: Dict, skills: List[str]) -> bool:
        job_text = job.get("description", "").lower()
        return any(skill.lower() in job_text for skill in skills)

    def _matches_experience(self, job: Dict) -> bool:
        # Posteriormente se podría mejorar esto con NLP después, pero por ahora va básico.
        return "junior" in job.get("description", "").lower() or "0-2 years" in job.get("description", "").lower()

    def _has_negative_keywords(self, job: Dict) -> bool:
        job_text = job.get("description", "").lower()
        return any(kw in job_text for kw in self.negative_keywords)
