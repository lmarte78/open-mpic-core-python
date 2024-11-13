from abc import ABC
from typing import Literal, Union

from typing_extensions import Annotated

from open_mpic_core.common_domain.enum.check_type import CheckType
from pydantic import BaseModel, model_validator, Field

from open_mpic_core.mpic_coordinator.domain.mpic_orchestration_parameters import MpicRequestOrchestrationParameters
from open_mpic_core.common_domain.check_parameters import CaaCheckParameters, DcvCheckParameters


class BaseMpicRequest(BaseModel, ABC):
    domain_or_ip_target: str
    check_type: CheckType
    orchestration_parameters: MpicRequestOrchestrationParameters | None = None


class MpicCaaRequest(BaseMpicRequest):
    check_type: Literal[CheckType.CAA] = CheckType.CAA
    caa_check_parameters: CaaCheckParameters | None = None


class MpicDcvRequest(BaseMpicRequest):
    check_type: Literal[CheckType.DCV] = CheckType.DCV
    dcv_check_parameters: DcvCheckParameters


MpicRequest = Annotated[Union[MpicCaaRequest, MpicDcvRequest], Field(discriminator='check_type')]
