# coding: utf-8

#
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License'). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#
from __future__ import absolute_import

from .distribution_mode import DistributionMode
from .game_engine_interface import GameEngineInterface
from .video_region import VideoRegion
from .tax_information import TaxInformation
from .music_wordmark import MusicWordmark
from .video_feature import VideoFeature
from .amazon_conversations_dialog_manager import AMAZONConversationsDialogManager
from .custom_task import CustomTask
from .supported_controls_type import SupportedControlsType
from .skill_manifest_apis import SkillManifestApis
from .custom_apis import CustomApis
from .locales_by_automatic_cloned_locale import LocalesByAutomaticClonedLocale
from .alexa_for_business_interface import AlexaForBusinessInterface
from .dialog_management import DialogManagement
from .skill_manifest_publishing_information import SkillManifestPublishingInformation
from .music_content_name import MusicContentName
from .permission_name import PermissionName
from .flash_briefing_apis import FlashBriefingApis
from .region import Region
from .manifest_version import ManifestVersion
from .viewport_specification import ViewportSpecification
from .shopping_kit import ShoppingKit
from .alexa_for_business_interface_request_name import AlexaForBusinessInterfaceRequestName
from .localized_flash_briefing_info import LocalizedFlashBriefingInfo
from .event_name_type import EventNameType
from .smart_home_apis import SmartHomeApis
from .linked_common_schemes import LinkedCommonSchemes
from .interface_type import InterfaceType
from .friendly_name import FriendlyName
from .subscription_information import SubscriptionInformation
from .music_alias import MusicAlias
from .distribution_countries import DistributionCountries
from .display_interface_template_version import DisplayInterfaceTemplateVersion
from .health_interface import HealthInterface
from .extension_request import ExtensionRequest
from .music_feature import MusicFeature
from .voice_profile_feature import VoiceProfileFeature
from .event_publications import EventPublications
from .viewport_mode import ViewportMode
from .audio_interface import AudioInterface
from .skill_manifest import SkillManifest
from .flash_briefing_content_type import FlashBriefingContentType
from .authorized_client import AuthorizedClient
from .gadget_controller_interface import GadgetControllerInterface
from .catalog_info import CatalogInfo
from .music_interfaces import MusicInterfaces
from .custom_connections import CustomConnections
from .video_prompt_name import VideoPromptName
from .localized_flash_briefing_info_items import LocalizedFlashBriefingInfoItems
from .free_trial_information import FreeTrialInformation
from .gadget_support_requirement import GadgetSupportRequirement
from .android_common_intent_name import AndroidCommonIntentName
from .music_capability import MusicCapability
from .manifest_gadget_support import ManifestGadgetSupport
from .up_channel_items import UpChannelItems
from .alexa_for_business_apis import AlexaForBusinessApis
from .skill_manifest_localized_publishing_information import SkillManifestLocalizedPublishingInformation
from .extension_initialization_request import ExtensionInitializationRequest
from .version import Version
from .video_app_interface import VideoAppInterface
from .paid_skill_information import PaidSkillInformation
from .alexa_search import AlexaSearch
from .lambda_region import LambdaRegion
from .connections_payload import ConnectionsPayload
from .flash_briefing_genre import FlashBriefingGenre
from .linked_application import LinkedApplication
from .dialog_delegation_strategy import DialogDelegationStrategy
from .app_link_interface import AppLinkInterface
from .permission_items import PermissionItems
from .demand_response_apis import DemandResponseApis
from .marketplace_pricing import MarketplacePricing
from .play_store_common_scheme_name import PlayStoreCommonSchemeName
from .knowledge_apis import KnowledgeApis
from .app_link import AppLink
from .source_language_for_locales import SourceLanguageForLocales
from .catalog_type import CatalogType
from .viewport_shape import ViewportShape
from .linked_android_common_intent import LinkedAndroidCommonIntent
from .catalog_name import CatalogName
from .android_custom_intent import AndroidCustomIntent
from .subscription_payment_frequency import SubscriptionPaymentFrequency
from .automatic_distribution import AutomaticDistribution
from .lambda_endpoint import LambdaEndpoint
from .custom_product_prompts import CustomProductPrompts
from .video_catalog_info import VideoCatalogInfo
from .dialog_manager import DialogManager
from .automatic_cloned_locale import AutomaticClonedLocale
from .authorized_client_lwa_application import AuthorizedClientLwaApplication
from .event_name import EventName
from .video_country_info import VideoCountryInfo
from .skill_manifest_envelope import SkillManifestEnvelope
from .display_interface import DisplayInterface
from .music_request import MusicRequest
from .alexa_presentation_apl_interface import AlexaPresentationAplInterface
from .flash_briefing_update_frequency import FlashBriefingUpdateFrequency
from .video_prompt_name_type import VideoPromptNameType
from .skill_manifest_endpoint import SkillManifestEndpoint
from .localized_name import LocalizedName
from .currency import Currency
from .house_hold_list import HouseHoldList
from .interface import Interface
from .skill_manifest_localized_privacy_and_compliance import SkillManifestLocalizedPrivacyAndCompliance
from .custom_localized_information_dialog_management import CustomLocalizedInformationDialogManagement
from .knowledge_apis_enablement_channel import KnowledgeApisEnablementChannel
from .display_interface_apml_version import DisplayInterfaceApmlVersion
from .app_link_v2_interface import AppLinkV2Interface
from .smart_home_protocol import SmartHomeProtocol
from .ios_app_store_common_scheme_name import IOSAppStoreCommonSchemeName
from .authorized_client_lwa import AuthorizedClientLwa
from .video_apis_locale import VideoApisLocale
from .video_fire_tv_catalog_ingestion import VideoFireTvCatalogIngestion
from .skill_manifest_events import SkillManifestEvents
from .ssl_certificate_type import SSLCertificateType
from .custom_localized_information import CustomLocalizedInformation
from .lambda_ssl_certificate_type import LambdaSSLCertificateType
from .localized_knowledge_information import LocalizedKnowledgeInformation
from .supported_controls import SupportedControls
from .tax_information_category import TaxInformationCategory
from .authorized_client_lwa_application_android import AuthorizedClientLwaApplicationAndroid
from .localized_music_info import LocalizedMusicInfo
from .music_apis import MusicApis
from .skill_manifest_privacy_and_compliance import SkillManifestPrivacyAndCompliance
from .offer_type import OfferType
from .video_apis import VideoApis
from .alexa_for_business_interface_request import AlexaForBusinessInterfaceRequest
from .alexa_presentation_html_interface import AlexaPresentationHtmlInterface
from .music_content_type import MusicContentType
