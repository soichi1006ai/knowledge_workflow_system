class ValidationService:
    """
    Frontmatter is canonical source of truth.
    system/index/* is rebuildable cache and not required for primary validation.
    """

    def validate_archive_rule(self) -> None:
        return None

    def validate_related_rule(self) -> None:
        return None

    def validate_source_of_truth_rule(self) -> None:
        return None
