import sys
import pytest

from open_mpic_core import DcvValidationMethod, RemotePerspective, MpicRequestValidationMessages, MpicRequestValidator

from unit.test_util.valid_mpic_request_creator import ValidMpicRequestCreator


# noinspection PyMethodMayBeStatic
class TestMpicRequestValidator:
    @classmethod
    def setup_class(cls):
        cls.known_perspectives = [
            RemotePerspective(rir="rir1", code="p1"),
            RemotePerspective(rir="rir1", code="p2"),
            RemotePerspective(rir="rir1", code="p3"),
            RemotePerspective(rir="rir1", code="p4"),
            RemotePerspective(rir="rir2", code="p5"),
            RemotePerspective(rir="rir2", code="p6"),
            RemotePerspective(rir="rir2", code="p7"),
            RemotePerspective(rir="rir2", code="p8"),
            RemotePerspective(rir="rir3", code="p9"),
            RemotePerspective(rir="rir3", code="p10"),
        ]

    def is_request_valid__should_be_true_and_empty_list_given_valid_caa_check_request_with_perspective_count(self):
        request = ValidMpicRequestCreator.create_valid_caa_mpic_request()
        is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(request, self.known_perspectives)
        assert is_request_valid is True
        assert len(validation_issues) == 0

    def is_request_valid__should_be_true_given_valid_caa_check_without_orchestration_parameters_or_check_details(self):
        request = ValidMpicRequestCreator.create_valid_caa_mpic_request()
        request.orchestration_parameters = None
        request.caa_check_parameters = None
        is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(request, self.known_perspectives)
        assert is_request_valid is True
        assert len(validation_issues) == 0

    @pytest.mark.parametrize(
        "validation_method", [DcvValidationMethod.DNS_CHANGE, DcvValidationMethod.WEBSITE_CHANGE_V2]
    )
    def is_request_valid__should_be_true_given_valid_dcv_check_request(self, validation_method):
        request = ValidMpicRequestCreator.create_valid_dcv_mpic_request(validation_method)
        is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(request, self.known_perspectives)
        assert is_request_valid is True
        assert len(validation_issues) == 0

    @pytest.mark.parametrize("perspective_count", [1, 0, -1, "abc", sys.maxsize + 1])
    def is_request_valid__should_be_false_with_message_given_invalid_perspective_count(self, perspective_count):
        request = ValidMpicRequestCreator.create_valid_caa_mpic_request()
        request.orchestration_parameters.perspective_count = perspective_count
        is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(request, self.known_perspectives)
        assert is_request_valid is False
        issue_type = MpicRequestValidationMessages.INVALID_PERSPECTIVE_COUNT.key
        assert issue_type in [issue.issue_type for issue in validation_issues]
        invalid_perspective_count_issue = next(issue for issue in validation_issues if issue.issue_type == issue_type)
        assert str(perspective_count) in invalid_perspective_count_issue.message

    # TODO should there be a more permissive validation (in diagnostic mode?) for quorum count?
    @pytest.mark.parametrize("quorum_count", [1, -1, 0, 10, "abc", sys.maxsize + 1])
    def is_request_valid__should_be_false_with_message_given_invalid_quorum_count(self, quorum_count):
        request = ValidMpicRequestCreator.create_valid_caa_mpic_request()
        request.orchestration_parameters.quorum_count = quorum_count
        is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(request, self.known_perspectives)
        assert is_request_valid is False
        issue_type = MpicRequestValidationMessages.INVALID_QUORUM_COUNT.key
        assert issue_type in [issue.issue_type for issue in validation_issues]
        invalid_quorum_count_issue = next(issue for issue in validation_issues if issue.issue_type == issue_type)
        assert str(quorum_count) in invalid_quorum_count_issue.message

    # @pytest.mark.parametrize('challenge_value, match_regex, expected_is_request_valid, error_message', [
    #     ('', '', False, MpicRequestValidationMessages.EMPTY_CHALLENGE_VALUE),
    #     ('', '.*', True, None),
    #     ('abc', '.*', True, None),
    #     ('abc', '', True, None),
    # ])
    # def is_request_valid__should_be_false_and_message_given_empty_challenge_value_unless_match_regex_set(
    #         self, challenge_value, match_regex, expected_is_request_valid, error_message
    # ):
    #     request = ValidMpicRequestCreator.create_valid_dcv_mpic_request(DcvValidationMethod.WEBSITE_CHANGE_V2)
    #     request.dcv_check_parameters.validation_details.challenge_value = challenge_value
    #     # request.dcv_check_parameters.validation_details.match_regex = match_regex
    #     is_request_valid, validation_issues = MpicRequestValidator.is_request_valid(request, self.known_perspectives)
    #     assert is_request_valid is expected_is_request_valid
    #     if error_message is not None:
    #         assert error_message.key in [issue.issue_type for issue in validation_issues]
    #         assert error_message.message in [issue.message for issue in validation_issues]


if __name__ == "__main__":
    pytest.main()
