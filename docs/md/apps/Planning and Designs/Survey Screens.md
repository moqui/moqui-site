# Survey Screens

NOTE: These screens are implemented in SimpleScreens Survey (`/qapps/marble/Survey`).

- Find Survey
    - create dialog with simple form
    - survey list (DbForm with purposeEnumId=DbfpSurvey)
- Survey tab (EditSurvey)
    - edit form (for DbForm; only description and comments fields)
    - User Groups section (right column)
        - add dialog (DbFormUserGroup)
        - list/edit form-list
- Fields tab
    - form at top to add field
    - list fields in section-iterate (not form-list)
        - field info edit form (DbFormField; skip print fields; in left column)
        - field options (shown if fieldTypeEnumId in DBFFT_check, DBFFT_drop, DBFFT_radio; DbFormFieldOption; in right column)
- Responses
    - list/find form
    - response detail screen with all answers
- Response Stats
    - for enumerated options show counts for each option
    - for text fields show count of non empty
