#!/usr/bin/env python3
import boto3
import click


def listMembers(session):
    """Lists member accounts that are associated with Security Hub

    Args:
      session: boto3 session

    Returns:
      Returns a list of account email addresses and AccountIds
    """

    sh_client = session.client('securityhub')
    counter = 0

    # use paginator if more than 1000 results or memory issues with the results
    paginator = sh_client.get_paginator('list_members')
    results = []

    for page in paginator.paginate(OnlyAssociated=True):
        results += page.get('Members', [])

    for result in results:
        email = result.get('Email')
        accountID = result.get('AccountId')
        print(accountID, email)
        if email is None:
            counter += 1

    print(counter, 'accounts have no email')


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--profile', required=True, default='default', help='AWS profile from ~/.aws/config or ~/.aws/credentials')
def main(profile):
    # For SSO profiles, enter <account name>.<role name>
    session = boto3.session.Session(profile_name=profile)
    listMembers(session)


if __name__ == '__main__':
    main()
