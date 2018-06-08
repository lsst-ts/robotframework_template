*** Settings ***
Documentation    This resource file defines common keywords used by all the SAL test suites.
Library    Library/FILLMEIN_SAL.py

*** Keywords ***
Verify Summary State Event
    [Arguments]    ${expectedState}
    Comment    Every sub-State transition triggers a Summary State Event.
    ${valid}    ${data}=    Get Event Summary State
    Log    ${data.Timestamp}
    Log    ${data.SummaryState}
    Should Be True    ${valid}
    Should Be Equal As Integers    ${data.SummaryState}    ${expectedState}

Verify Detailed State Event 
    [Arguments]    ${expectedState}
    Comment    Every State transition triggers a Detailed State Event.
    ${valid}    ${data}=    Get Event Detailed State
    Log    ${data.Timestamp}
    Log    ${data.DetailedState}
    Should Be True    ${valid}
    Should Be Equal As Integers    ${data.DetailedState}    ${expectedState}

Get Event
    [Arguments]    ${EventTopic}
    Comment    Events are queued until read. Query the topic until the most recent event is returned.
    : FOR    ${INDEX}    IN RANGE    1    1000
    \    ${valid}    ${data}=    Run Keyword    Get Event ${EventTopic}
    \    Run Keyword If    ${valid}    Exit For Loop
    \    Sleep    10ms
    [Return]    ${valid}    ${data}

Verify Timestamp 
    [Arguments]    ${timestamp}=${0}
    Comment    Get current time in epoch.
    ${epoch}=    Get Current Date    result_format=epoch
    Comment    Verify timestamp.
    Should Be True    ${timestamp} > ${epoch}
