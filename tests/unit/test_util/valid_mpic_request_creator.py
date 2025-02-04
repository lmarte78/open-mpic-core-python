from open_mpic_core.common_domain.check_parameters import CaaCheckParameters, DcvCheckParameters, \
    DcvDnsChangeValidationParameters, DcvWebsiteChangeValidationParameters, DcvAcmeDns01ValidationParameters, \
    DcvAcmeHttp01ValidationParameters, DcvContactPhoneCaaValidationParameters, DcvContactPhoneTxtValidationParameters, \
    DcvContactEmailTxtValidationParameters, DcvContactEmailCaaValidationParameters
from open_mpic_core.common_domain.enum.certificate_type import CertificateType
from open_mpic_core.common_domain.enum.dcv_validation_method import DcvValidationMethod
from open_mpic_core.common_domain.enum.dns_record_type import DnsRecordType
from open_mpic_core.common_domain.enum.url_scheme import UrlScheme
from open_mpic_core.mpic_coordinator.domain.mpic_request import MpicRequest
from open_mpic_core.common_domain.enum.check_type import CheckType
from open_mpic_core.mpic_coordinator.domain.mpic_request import MpicCaaRequest
from open_mpic_core.mpic_coordinator.domain.mpic_request import MpicDcvRequest
from open_mpic_core.mpic_coordinator.domain.mpic_orchestration_parameters import MpicRequestOrchestrationParameters


class ValidMpicRequestCreator:
    @staticmethod
    def create_valid_caa_mpic_request() -> MpicCaaRequest:
        return MpicCaaRequest(
            domain_or_ip_target='test.example.com',
            orchestration_parameters=MpicRequestOrchestrationParameters(perspective_count=6, quorum_count=4),
            caa_check_parameters=CaaCheckParameters(certificate_type=CertificateType.TLS_SERVER)
        )

    @staticmethod
    def create_valid_dcv_mpic_request(validation_method=DcvValidationMethod.DNS_CHANGE) -> MpicDcvRequest:
        return MpicDcvRequest(
            domain_or_ip_target='test.example.com',
            orchestration_parameters=MpicRequestOrchestrationParameters(perspective_count=6, quorum_count=4),
            dcv_check_parameters=ValidMpicRequestCreator.create_check_parameters(validation_method)
        )

    @staticmethod
    def create_valid_mpic_request(check_type, validation_method=DcvValidationMethod.DNS_CHANGE) -> MpicRequest:
        match check_type:
            case CheckType.CAA:
                return ValidMpicRequestCreator.create_valid_caa_mpic_request()
            case CheckType.DCV:
                return ValidMpicRequestCreator.create_valid_dcv_mpic_request(validation_method)

    @classmethod
    def create_check_parameters(cls, validation_method=DcvValidationMethod.DNS_CHANGE, dns_record_type=DnsRecordType.TXT):
        check_parameters = None
        match validation_method:
            case DcvValidationMethod.DNS_CHANGE:
                check_parameters = DcvDnsChangeValidationParameters(dns_name_prefix='test', dns_record_type=dns_record_type, challenge_value='test')
            case DcvValidationMethod.WEBSITE_CHANGE:
                check_parameters = DcvWebsiteChangeValidationParameters(
                    http_token_path='examplepath', challenge_value='test', url_scheme=UrlScheme.HTTP)  # noqa E501 (http)
            case DcvValidationMethod.ACME_HTTP_01:
                check_parameters = DcvAcmeHttp01ValidationParameters(token='test', key_authorization='test')
            case DcvValidationMethod.ACME_DNS_01:
                check_parameters = DcvAcmeDns01ValidationParameters(key_authorization='test')
            case DcvValidationMethod.CONTACT_PHONE:
                if dns_record_type == DnsRecordType.CAA:
                    check_parameters = DcvContactPhoneCaaValidationParameters(dns_name_prefix='test', challenge_value='test')
                else:
                    check_parameters = DcvContactPhoneTxtValidationParameters(challenge_value='test')
            case DcvValidationMethod.CONTACT_EMAIL:
                if dns_record_type == DnsRecordType.CAA:
                    check_parameters = DcvContactEmailCaaValidationParameters(dns_name_prefix='test', challenge_value='test')
                else:
                    check_parameters = DcvContactEmailTxtValidationParameters(challenge_value='test')
        return check_parameters
