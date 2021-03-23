#!/usr/bin/env python3
import boto3
import click

def getInsights(session):
    """
    Docstring
    """

    sh_client = session.client('securityhub')
    # TODO make this useful
    response = sh_client.get_insights()
    print(response)

@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--profile', required=True, default='default', help='AWS profile from ~/.aws/config or ~/.aws/credentials')
def main(profile):
    # For SSO profiles, enter <account name>.<role name>
    session = boto3.session.Session(profile_name=profile)
    getInsights(session)

if __name__ == '__main__':
   # profile_name = 'default'
    main()
