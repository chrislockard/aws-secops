#!/usr/bin/env python3
import boto3
import time


def query(session):
    """
    Docstring
    """

    gd_client = session.client('guardduty')

    detector = gd_client.list_detectors()
    detectorid = detector['DetectorIds'][0]

    # Change to number of previous days to search
    days = 5
    search_from_time = int(time.time())-(days*(86400))

    # Finding criteria should be changed to include interesting criteria pulled from
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Client.create_filter
    rank_one = {'Criterion': {'severity': {'Gte': 1}}}
    s3_public_access = {'Criterion': {'resource.s3BucketDetails.publicAccess.effectivePermission': {'Equals': ['PUBLIC']}, 'updatedAt': {'Gte': search_from_time}}}
    search_by_time = {'Criterion': {'updatedAt': {'Gte': search_from_time}}}
    fc = search_by_time

    # Create paginator for GD list_findings API
    paginator = gd_client.get_paginator('list_findings')

    # Response iterator holds all pages
    response_iterator = paginator.paginate(
        DetectorId=detectorid, FindingCriteria=fc)

    # gd_findings holds all finding ids across all pages
    gd_findings = []
    
    # finding_results holds results of all findings
    finding_results = []

    for page in response_iterator:
        # Iterate through pages and aggregate finding IDs
        for finding in page.get('FindingIds', {}):
            gd_findings.append(finding)

    # Iterate through finding IDs and retrive details
    # Return details from Findings as a list
    # see https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#GuardDuty.Client.get_findings
    for finding in gd_findings:
        finding_results += gd_client.get_findings(
            DetectorId=detectorid, FindingIds=[finding]).get('Findings', [])

    # Post-processing goes here, by default print to stdout
    # Here, looks for instances where BPA was disabled
    for result in finding_results:
        if 'Amazon S3 Block Public Access was disabled for' in result.get('Description', ''):
            print(result)


if __name__ == '__main__':
    # For SSO profiles, enter <account name>.<role name>
    # TODO sort by account id, sort by event type, sort by time and generate trending
    # of events by type in an account over time
    profile_name = '<account name>.<role name>'
    session = boto3.session.Session(profile_name=profile_name)
    query(session)
