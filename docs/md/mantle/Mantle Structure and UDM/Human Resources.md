# Human Resources
[TOC levels=2]

## Ability (mantle.humanres.ability)

The most general representation of ability is PartyResume which may have the full text in the **resumeText** field or may point to a Resource Facade **contentLocation**.

Getting more structured the PartyQualification entity is used for things like degrees, certifications, and work experience. The types available (**qualificationTypeEnumId**) are Enumeration records of type QualificationType and you can add any needed there. It has a verificationStatusId for tracking verification, and a more general status (**statusId**) that can be Completed, Incomplete, or Deferred for things like degrees and certifications, and Full-time, Part-time, or Contractor for things like work experience.

PartySkill is for more specific skills as opposed to more general qualifications. This would include things like specific programming languages and libraries, equipment operation, and even creative talents. The skill types (**skillTypeEnumId**) are Enumeration records of type SkillType. This has fields about the skill such as **yearsExperience**, **skillLevel**, and **startedUsingDate**.

A PerformanceReview is between a manager (**managerPartyId**) and employee (**employeePartyId**) for a particular position (**emplPositionId**). It has items (PerformanceReviewItem) of various types (**reviewItemTypeEnumId**) such as Responsibility, Attitude, and Job Satisfaction with a rating (**reviewRatingEnumId**) and **comments** for each. Outside the context of a review there may also be performance notes recorded with the PerformanceNote entity.

To track employer sponsored and other training use the TrainingClass entity for classes available and PersonTraining for classes to approve and/or actually completed.

## Employment (mantle.humanres.employment)

The Employment entity is used to track employment of an employee by an employer in a certain position (**emplPositionId**). It shares its primary key (**partyRelationshipId**) with a PartyRelationship between the employee (**fromPartyId**) and the internal organization (**toPartyId**) with **relationshipTypeEnumId**=PrtEmployee; the employment date range (**fromDate**, **thruDate**) is on that relationship. When employment is terminated it can track a reason (**terminationReasonEnumId**) and type (**terminationTypeEnumId**).

Benefits of BenefitType may be tracked with EmploymentBenefit, and the relevant PayGrade with EmploymentSalary. Tax and payroll withholding defaults live on the Employee entity and may be overridden on Employment.

Before employment there may be an application (EmploymentApplication) by an applicant (**applyingPartyId**) for a position (**emplPositionId**).

After employment any unemployment claims would be tracked with UnemploymentClaim.

## Position (mantle.humanres.position)

An EmplPosition is a specific position within an organization (**organizationPartyId**). The employee in the position is tracked with Employment (and the related PartyRelationship); for other parties associated with the position such as manager or department use the EmplPositionParty entity. EmplPosition has a pay grade (**payGradeId**), may be part of a budget (**budgetId**, **budgetItemSeqId**) and may be planned for a date range (**fromDate**, **thruDate**).

A position is associated with an employment position class (**emplPositionClassId** pointing to EmplPositionClass) like Programmer, Business Analyst, Project Manager, and so on. It is common to have multiple positions for a class, and a class can exist separately and be associated directly with parties (EmplPositionClassParty) for a simplified model for rate determination and such that does not require an EmplPosition record.

Responsibilities such as Finance Management, Inventory Management, and Purchase Management may be associated with a position using EmplPositionResponsibility or with a class using EmplClassResponsibility. A few responsibilities are defined OOTB and additional ones may be defined with Enumeration records of type EmploymentResponsibility.

## Rate (mantle.humanres.rate)

Within an organization it is often useful to standardize pay grades. Use the PayGrade entity for pay grades available, and PayGradeSalary for the actual pay **amount** within a date range (**fromDate**, **thruDate**).

For more detailed and structured pay rate information use the RateAmount entity. This can be used for billing rates to clients for services performed, and payment to external vendors if applicable for actually performing services (**ratePurposeEnumId**). Rate types (**rateTypeEnumId**) include Standard, Discounted, Overtime, and On-site Work.

The **rateAmount** (with currency **rateCurrencyUomId** and for time unit **timePeriodUomId**) is valid within a date range (**fromDate**, **thruDate**) and may be restricted to a particular Party (**partyId**), WorkEffort (**workEffortId**), and position class (**emplPositionClassId**).

## Recruitment (mantle.humanres.recruitment)

The recruitment process will often begin with creating a JobRequisition and one or more EmplPosition records for the requisition. Typically EmploymentApplication records are next to apply for the position, and then for some of the applications zero to many JobInterview records, one for each interview done with the candidate (**candidatePartyId**) by an interviewer (**interviewerPartyId**). For each position an Employment record is created when a candidate is hired.
