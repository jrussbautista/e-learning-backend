class CourseStatus:
    DRAFT = "draft"
    FOR_REVIEW = "for_review"
    ACTIVE = "active"


    choices = (
        (DRAFT, "Draft"),
        (FOR_REVIEW, "For Review"),
        (ACTIVE, "Active")
    )
