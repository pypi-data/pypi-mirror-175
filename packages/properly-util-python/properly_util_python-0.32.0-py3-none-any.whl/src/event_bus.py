import json
import os
from enum import Enum

import boto3

from src.environments import get_properly_stage_for_resource
from src.properly_logging import ProperLogger


class ProperlyEvents(str, Enum):
    USER_CREATED = "userCreated"
    USER_CITY_UPDATED = "userCityUpdated"
    USER_ALERT_UNSUBSCRIBED = "userAlertUnsubscribed"
    STAGE_CHANGED_OFFER = "stageChangedOffer"
    USER_ENTERED_ALL_OFFER_INFO = "userEnteredAllOfferInfo"
    SHOWING_UPDATED_OR_CREATED = "userShowingUpdatedOrCreated"
    HUBSPOT_DEAL_CHANGED = "hubspotDealChanged"
    DEAL_CHANGED_STAGE = "dealChangedStage"
    ACCEPTED_OFFER = "userAcceptedOffer"
    SEARCH_RESULTS_CHANGED = "searchResultsChanged"
    RECOMMENDATION_RESULTS_CHANGED = "recommendationResultsChanged"
    PPR_FEEDBACK = "pprFeedback"
    FAVOURITE_ADDED = "favouriteAdded"
    FAVOURITE_REMOVED = "favouriteRemoved"
    USER_DEAL_STAGES_CHANGED = "userDealStagesChanged"
    BEHAVIOUR_TRACK_EVENT = "behaviourTrackEvent"
    COGNITO_ACCOUNT_MESSAGE = "cognitoAccountMessage"
    ASK_AGENT_A_QUESTION = "askAgentAQuestion"
    SUBSCRIBE_TO_MARKETING_EMAIL = "subscribeToMarketingEmail"
    UNSUBSCRIBE_FROM_MARKETING_EMAIL = "unsubscribeFromMarketingEmail"


class EventBusBase:
    def send_event(self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict):
        raise NotImplementedError

    def send_event_async(
        self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict
    ):
        raise NotImplementedError


class PropertyEvents(str, Enum):
    PROPERTY_VERIFIED_INFO_UPDATED = "propertyVerifiedInfoUpdated"
    PPR_ESTIMATE_UPDATE = "pprEstimateUpdated"


class HistoricalPropertyEvents(str, Enum):
    HISTORICAL_PROPERTY_UPDATED = "historicalPropertyUpdated"


class NamedEventBus(EventBusBase):
    def __init__(self, stream_name, kinesis=None, logger=None, ignore_custom_stages=True):
        stage = get_properly_stage_for_resource(use_local_for_tests=True, ignore_custom_stages=ignore_custom_stages)
        self.kinesis = kinesis or boto3.client("kinesis")
        self.stream_name = f"{stage}-{stream_name}"
        self.logger = logger if logger else ProperLogger("NamedEventBus")

    def send_event(self, partition_key: str, event_name: str, data_block_name: str, data_block: dict):
        event_to_send = {"eventName": event_name, data_block_name: data_block}
        self.logger.debug("Sending event", {"event": event_to_send})

        event_as_json = json.dumps(event_to_send)
        event_as_bytes = event_as_json.encode("utf-8")

        # Kinesis data payloads are in bytes in base64 encoded
        self.logger.debug("Event as bytes", {"event_as_bytes": event_as_bytes})
        self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=event_as_bytes,
            PartitionKey=partition_key,
        )

    async def send_event_async(self, partition_key: str, event_name: str, data_block_name: str, data_block: dict):
        event_to_send = {"eventName": event_name, data_block_name: data_block}
        self.logger.debug("Sending event", {"event": event_to_send})

        event_as_json = json.dumps(event_to_send)
        event_as_bytes = event_as_json.encode("utf-8")

        # Kinesis data payloads are in bytes in base64 encoded
        self.logger.debug("Event as bytes", {"event_as_bytes": event_as_bytes})
        return await self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=event_as_bytes,
            PartitionKey=partition_key,
        )


class PropertyEventBus(NamedEventBus):
    """
    This the wrapped up implementation of the event bus for Property records.
    """

    def send_event(self, property_id: str, event_name: PropertyEvents, data_block_name: str, data_block: dict):
        """
        The send event for the Property related buses.
        :param property_id: The Property ID of the record. This is used as the bus partition key.
        :param event_name: The name of the bus event.
        :param data_block_name: The attribute name of the data block.
        :param data_block: The block of data put on the bus.
        """
        super().send_event(
            partition_key=property_id, event_name=event_name, data_block_name=data_block_name, data_block=data_block
        )

    async def send_event_async(
        self, property_id: str, event_name: PropertyEvents, data_block_name: str, data_block: dict
    ):
        """
        The async send event for the Property related buses.
        :param property_id: The Property ID of the record. This is used as the bus partition key.
        :param event_name: The name of the bus event.
        :param data_block_name: The attribute name of the data block.
        :param data_block: The block of data put on the bus.
        """
        return await super().send_event_async(
            partition_key=property_id, event_name=event_name, data_block_name=data_block_name, data_block=data_block
        )


class EventBus(NamedEventBus):
    def __init__(self, kinesis=None, logger=None, ignore_custom_stages=True):
        """
        The default generic event bus handler for "events-002" Kinesis stream.
        """
        super().__init__(
            stream_name="events-002", kinesis=kinesis, logger=logger, ignore_custom_stages=ignore_custom_stages
        )

    def send_event(self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict):
        """
        The send event for the default user related buses.
        :param properly_user_id: The user ID of the record.  This is used as the partition key.
        :param event_name: The name of the bus event.
        :param data_block_name: The attribute name of the data block.
        :param data_block: The block of data put on the bus.
        """
        super().send_event(
            partition_key=properly_user_id,
            event_name=event_name,
            data_block_name=data_block_name,
            data_block=data_block,
        )

    async def send_event_async(
        self, properly_user_id: str, event_name: ProperlyEvents, data_block_name: str, data_block: dict
    ):
        """
        The async send event for the default user related buses.
        :param properly_user_id: The user ID of the record.  This is used as the partition key.
        :param event_name: The name of the bus event.
        :param data_block_name: The attribute name of the data block.
        :param data_block: The block of data put on the bus.
        """
        return await super().send_event_async(
            partition_key=properly_user_id,
            event_name=event_name,
            data_block_name=data_block_name,
            data_block=data_block,
        )
