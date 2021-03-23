#!/usr/bin/env python3
import boto3
import click

def listMembers(session):
    """
    Docstring
    """

    sh_client = session.client('securityhub')
    # TODO make this useful
    response = sh_client.list_members(OnlyAssociated=True)
    print(response)

@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--profile', required=True, default='default', help='AWS profile from ~/.aws/config or ~/.aws/credentials')
def main(profile):
    # For SSO profiles, enter <account name>.<role name>
    session = boto3.session.Session(profile_name=profile)
    listMembers(session)

if __name__ == '__main__':
   # profile_name = 'default'
    main()
