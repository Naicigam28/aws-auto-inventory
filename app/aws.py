# -*- coding: utf-8 -*-
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

#   Licensed under the Apache License, Version 2.0 (the "License").
#   You may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging
import boto3


log = logging.getLogger("aws-auto-inventory.aws")


def fetch(session, region_name, service, function, result_key, parameters):
    log.info(
        "Started: {}:{}:{}:{}:{}".format(
            region_name, service, function, result_key, parameters
        )
    )
    response = ""

    try:
        # session = boto3.Session(profile_name=profile_name)
        client = session.client(service, region_name=region_name)

        if parameters is not None:
            if result_key:
                response = client.__getattribute__(function)(**parameters).get(
                    result_key
                )
            else:
                response = client.__getattribute__(function)(**parameters)
        elif result_key:
            response = client.__getattribute__(function)().get(result_key)
        else:
            response = client.__getattribute__(function)()
            # Remove ResponseMetadata as it's not useful
            response.pop("ResponseMetadata", None)

    except Exception as e:
        log.error("Error while processing {}, {}.\n{}".format(service, region_name, e))

    log.info("Finished:{}:{}:{}:{}".format(service, region_name, function, result_key))
    return response


# def get_methods(client):
#     methods = dir(client)
#     return methods


# def get_read_methods(client):
#     list = []
#     methods = get_methods(client)
#     for method in methods:
#         if "describe" in method or "list" in method:
#             list.append(method)
#     return list


def get(session, region_name, sheet):
    # results = []

    service = sheet["service"]
    function = sheet["function"]

    # optional
    result_key = sheet.get("result_key", None)
    parameters = sheet.get("parameters", None)

    # log.info(
    #     "Started:{}:{}:{}:{}:{}".format(region_name, service, function, result_key)
    # )

    result = fetch(
        session=session,
        region_name=region_name,
        service=service,
        function=function,
        result_key=result_key,
        parameters=parameters,
    )
    # results.append(result)
    log.info("Result:{{{}}}".format(result))
    log.info("Finished:{}:{}:{}:{}".format(region_name, service, function, result_key))

    return result


def get_session():
    """Return an AWS session"""

    log.info("Started: Get AWS Session")
    session = boto3.Session()
    # session = boto3.Session(profile_name=profile_name)
    client = session.client("sts")
    response = client.get_caller_identity()
    log.info("Response: %s", response)

    log.info("Started: Get AWS Session")
    return session


# def get_account_id(profile_name):
#     log.info("Started:get_caller_identity")

#     session = boto3.Session(profile_name=profile_name)
#     client = session.client(service_name="sts")
#     response = client.get_caller_identity()
#     account = response["Account"]
#     user_id = response["UserId"]
#     arn = response["Arn"]

#     log.info("Account: {}".format(account))
#     log.info("UserId: {}".format(user_id))
#     log.info("Arn: {}".format(arn))

#     log.info("Finished: get_caller_identity")
#     return account
