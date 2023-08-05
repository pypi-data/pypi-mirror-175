import typing

import dso.labels
import dso.cvss
import protecode.model as pm


def _components_with_cves(
    result: pm.AnalysisResult
) -> typing.Generator[tuple[pm.Component, list[pm.Vulnerability]], None, None]:
    '''
    yields two-tuples of components and unassessed, relevant CVEs
    '''
    for component in result.components():
        vulnerabilities = [
            v for v in component.vulnerabilities()
            if not v.historical() and not v.has_triage()
        ]

        if not vulnerabilities:
            continue

        yield component, sorted(vulnerabilities, key=lambda v: v.cve())


def _component_and_results_to_report_str(
    component: pm.Component,
    vulnerabilities: list[pm.Vulnerability],
    rescoring_rules: typing.Iterable[dso.cvss.RescoringRule] | None=None,
    cve_categorisation: dso.cvss.CveCategorisation | None=None,
) -> str:
    def vuln_str(vulnerability: pm.Vulnerability):
        if not rescoring_rules or not cve_categorisation or not vulnerability.cvss:
            rescore = False
        else:
            orig_sev = dso.cvss.CVESeverity.from_cve_score(vulnerability.cve_severity())
            rescored = dso.cvss.rescore(
                rescoring_rules=rescoring_rules,
                severity=orig_sev,
            )
            if orig_sev is rescored:
                rescore = False
            else:
                rescore = True

        v = vulnerability
        if not rescore:
            return f'{v.cve()} ({v.cve_severity()})'

        return f'{v.cve()} ({v.cve_severity()}) [rescore: {rescored.name}]'

    comp = f'{component.name()}:{component.version()}'
    vulns = ', '.join((
        vuln_str(v) for v in vulnerabilities
    ))

    report = f'`{comp}` - `{vulns}`'

    return report


def analysis_result_to_report_str(
    result: pm.AnalysisResult,
    rescoring_rules: typing.Iterable[dso.cvss.RescoringRule] | None=None,
    cve_categorisation: dso.cvss.CveCategorisation | None=None,
) -> str:
    components_and_cves = sorted(
        _components_with_cves(result=result),
        key=lambda comp_and_vulns: f'{comp_and_vulns[0].name()}:{comp_and_vulns[0].version()}',
    )

    return '\n'.join((
        _component_and_results_to_report_str(
            comp,
            results,
            rescoring_rules=rescoring_rules,
            cve_categorisation=cve_categorisation,
        )
        for comp, results in components_and_cves
    ))
