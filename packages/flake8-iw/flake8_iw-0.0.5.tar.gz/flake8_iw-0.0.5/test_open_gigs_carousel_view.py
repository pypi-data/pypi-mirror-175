from datetime import timedelta
from unittest.mock import PropertyMock, patch

from constance.test import override_config
from django.test import RequestFactory, TestCase
from django.urls import reverse
from expects import expect

from backend.models import CertificateType, UserProfile, WorkerCertificate, WorkerLevelLog
from backend.tests import factories
from backend.tests.matchers import have_context
from backend.worker_app_views import OpenGigsCarouselView
from w2.models import UserW2Document
from w2.tests import factories as w2_factories

from django.utils import timezone


class OpenGigsCarouselViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.worker = factories.UserProfileFactory()
        self.url = reverse("worker-app-open-gigs-carousel")
        self.request = self.factory.get(self.url)
        self.request.user = self.worker.user

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=False)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_disabled(self, mock_has_valid_or_in_review_vaccination_certificate):
        """
        When the promotion is disabled, don't show anything even when they meed the criteria
        """
        self.worker.w2_status = UserProfile.W2_STATUS_NONE
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = False
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_already_received(self, mock_has_valid_or_in_review_vaccination_certificate):
        """
        When they already have received the promo, don't show
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = False
        WorkerLevelLog.give_worker_promo(self.worker, WorkerLevelLog.LEVEL_PROMOTION_W2_VACCINATION)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch(
        "backend.worker_app_views.open_gigs_carousel_view.OpenGigsCarouselView.vaccination_w2_promotion_completed_on",
        new_callable=PropertyMock,
    )
    def test_w2_vaccination_promo_enabled_already_received_guess_vaxx_outside(
        self, mock_vaccination_w2_promotion_completed_on, mock_has_valid_or_in_review_vaccination_certificate
    ):
        """
        When they already have received the promo, don't show (even if promo wasn't saved)
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_vaccination_w2_promotion_completed_on.return_value = timezone.now() - timedelta(hours=72)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch(
        "backend.worker_app_views.open_gigs_carousel_view.OpenGigsCarouselView.vaccination_w2_promotion_completed_on",
        new_callable=PropertyMock,
    )
    def test_w2_vaccination_promo_enabled_already_received_guess_vaxx_within(
        self, mock_vaccination_w2_promotion_completed_on, mock_has_valid_or_in_review_vaccination_certificate
    ):
        """
        When they already have received the promo, show if we guess and it's within 24 hours
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_vaccination_w2_promotion_completed_on.return_value = timezone.now() - timedelta(hours=12)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch(
        "backend.worker_app_views.open_gigs_carousel_view.OpenGigsCarouselView.vaccination_w2_promotion_completed_on",
        new_callable=PropertyMock,
    )
    def test_w2_vaccination_promo_enabled_already_received_guess_w2_outside(
        self, mock_vaccination_w2_promotion_completed_on, mock_has_valid_or_in_review_vaccination_certificate
    ):
        """
        When they already have received the promo, show if we guess and it's within 24 hours
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        # update outside hook
        UserProfile.objects.filter(id=self.worker.id).update(date_modified=timezone.now() - timedelta(hours=72))
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_vaccination_w2_promotion_completed_on.return_value = timezone.now() - timedelta(hours=72)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_vaccination_certificate")
    @patch("backend.models.UserProfile.worked_shifts_count", new_callable=PropertyMock)
    def test_vaccination_card_disabled_when_w2_vaccination_promo_shown(
        self,
        mock_worked_shifts_count,
        mock_has_valid_vaccination_certificate,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the W2 Vaccination promo shows and we are supposed to show the vaccine upload, hide it instead
        """
        self.worker.w2_status = UserProfile.W2_STATUS_NONE
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = False
        mock_worked_shifts_count.return_value = 5
        mock_has_valid_vaccination_certificate.return_value = False
        mock_is_w2_enabled_for_worker_state.return_value = True
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_no_vaxx(
        self, mock_has_valid_or_in_review_vaccination_certificate, mock_is_w2_enabled_for_worker_state
    ):
        """
        When the promotion is enabled and they don't have vaxx but have W2, show it
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = False
        mock_is_w2_enabled_for_worker_state.return_value = True
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch("backend.models.WorkerLevelLog.worker_received_promo_on")
    def test_w2_vaccination_promo_enabled_show_when_complete_and_no_promo_date(
        self,
        mock_worker_received_promo_on,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but no promo is given (because of task)
        Hide the promo if we can't determine any good date to guess from (fallback)
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        mock_worker_received_promo_on.return_value = None
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_show_when_complete_and_no_promo_date_real(
        self,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but no promo is given (because of task) and both dates are within 24 hours
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        vaccine_certificate_type = factories.CertificateTypeFactory(
            name=CertificateType.CERTIFICATE_TYPE_VACCINATION_CERTIFICATE
        )
        factories.WorkerCertificateFactory(certificate_type=vaccine_certificate_type, worker=self.worker)
        w2_factories.UserW2DocumentFactory(user=self.worker)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_show_when_complete_and_no_promo_date_real_vax_outside(
        self,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but no promo is given (because of task) and vax date is over 24 hours
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        vaccine_certificate_type = factories.CertificateTypeFactory(
            name=CertificateType.CERTIFICATE_TYPE_VACCINATION_CERTIFICATE
        )
        cert = factories.WorkerCertificateFactory(
            certificate_type=vaccine_certificate_type,
            worker=self.worker,
        )
        WorkerCertificate.objects.filter(id=cert.id).update(created_at=timezone.now() - timedelta(hours=48))
        w2_factories.UserW2DocumentFactory(user=self.worker, status=UserW2Document.STATUS_COMPLETED)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_show_when_complete_and_no_promo_date_real_w2_outside(
        self,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but no promo is given (because of task) and w2 date is over 24 hours
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        vaccine_certificate_type = factories.CertificateTypeFactory(
            name=CertificateType.CERTIFICATE_TYPE_VACCINATION_CERTIFICATE
        )
        factories.WorkerCertificateFactory(
            certificate_type=vaccine_certificate_type,
            worker=self.worker,
        )
        w2doc = w2_factories.UserW2DocumentFactory(user=self.worker, status=UserW2Document.STATUS_COMPLETED)
        UserW2Document.objects.filter(id=w2doc.id).update(updated_at=timezone.now() - timedelta(hours=48))
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_show_when_complete_and_no_promo_date_real_both_outside(
        self,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but no promo is given (because of task) and both dates over 24 hours
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        vaccine_certificate_type = factories.CertificateTypeFactory(
            name=CertificateType.CERTIFICATE_TYPE_VACCINATION_CERTIFICATE
        )
        cert = factories.WorkerCertificateFactory(
            certificate_type=vaccine_certificate_type,
            worker=self.worker,
        )
        WorkerCertificate.objects.filter(id=cert.id).update(created_at=timezone.now() - timedelta(hours=48))
        w2doc = w2_factories.UserW2DocumentFactory(user=self.worker, status=UserW2Document.STATUS_COMPLETED)
        UserW2Document.objects.filter(id=w2doc.id).update(updated_at=timezone.now() - timedelta(hours=48))
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch("backend.models.WorkerLevelLog.worker_received_promo_on")
    def test_w2_vaccination_promo_enabled_show_within_24_hours(
        self,
        mock_worker_received_promo_on,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but it's less than 24 hours since
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        mock_worker_received_promo_on.return_value = timezone.now() - timedelta(hours=4)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    @patch("backend.models.WorkerLevelLog.worker_received_promo_on")
    def test_w2_vaccination_promo_enabled_hide_after_24_hours(
        self,
        mock_worker_received_promo_on,
        mock_has_valid_or_in_review_vaccination_certificate,
        mock_is_w2_enabled_for_worker_state,
    ):
        """
        When the promotion is enabled and they completed both but it's greater than 24 hours since
        """
        self.worker.w2_status = UserProfile.W2_STATUS_APPROVED
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        mock_worker_received_promo_on.return_value = timezone.now() - timedelta(hours=25)
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=False))

    @override_config(SHOW_VACCINATION_W2_PROMOTION_CARD=True)
    @patch("backend.models.UserProfile.is_w2_enabled_for_worker_state", new_callable=PropertyMock)
    @patch("backend.models.UserProfile.has_valid_or_in_review_vaccination_certificate", new_callable=PropertyMock)
    def test_w2_vaccination_promo_enabled_no_w2(
        self, mock_has_valid_or_in_review_vaccination_certificate, mock_is_w2_enabled_for_worker_state
    ):
        """
        When the promotion is enabledf and they have vaxx but not W2, show it
        """
        self.worker.w2_status = UserProfile.W2_STATUS_NONE
        self.worker.save()
        mock_has_valid_or_in_review_vaccination_certificate.return_value = True
        mock_is_w2_enabled_for_worker_state.return_value = True
        response = OpenGigsCarouselView.as_view()(self.request)
        expect(response).to(have_context(show_vaccination_w2_promotion=True))
