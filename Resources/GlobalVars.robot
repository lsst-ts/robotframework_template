*** Settings ***

*** Variables ***
${ContInt}				false
${UserName}				${EMPTY}
${PassWord}				${EMPTY}
${KeyFile}				${EMPTY}
${SALInstall}			/opt/sal
${SALHome}				${SalInstall}/lsstsal
${SALWorkDir}			${SalInstall}/test
${SALVersion}			0.0
${OpenspliceVersion}	6.7.170523OSS
${OpenspliceDate}		2017-06-21
${Prompt}				]$
${Host}					0.0.0.0

##### State Enumerations #####
${SummaryDisabled}		1
${SummaryEnabled}		2
${SummaryFault}			3
${SummaryOffline}		4
${SummaryStandby}		5
${DetailedDisabled}		1
${DetailedEnabled}		2
${DetailedFault}		3
${DetailedOffline}		4
${DetailedStandby}		5
