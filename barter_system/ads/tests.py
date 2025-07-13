from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ad, ExchangeProposal

class AdTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='testpass')
        self.other_user = User.objects.create_user(username='user2', password='testpass')
        self.ad = Ad.objects.create(
            user=self.user,
            title='Телефон',
            description='Рабочий телефон',
            category='Электроника',
            condition='used'
        )

    def test_create_ad(self):
        self.assertEqual(Ad.objects.count(), 1)
        self.assertEqual(self.ad.title, 'Телефон')

    def test_edit_ad(self):
        self.ad.title = 'Смартфон'
        self.ad.save()
        self.assertEqual(Ad.objects.get(pk=self.ad.pk).title, 'Смартфон')

    def test_delete_ad(self):
        self.ad.delete()
        self.assertEqual(Ad.objects.count(), 0)

    def test_filter_ad_by_category(self):
        ads = Ad.objects.filter(category='Электроника')
        self.assertIn(self.ad, ads)

class ProposalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.ad1 = Ad.objects.create(user=self.user1, title='Книга', description='...', category='Книги', condition='new')
        self.ad2 = Ad.objects.create(user=self.user2, title='Ноутбук', description='...', category='Электроника', condition='used')

    def test_create_proposal(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Обмен?',
            status='pending'
        )
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(proposal.status, 'pending')

    def test_update_proposal_status(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Обмен?',
            status='pending'
        )
        proposal.status = 'accepted'
        proposal.save()
        self.assertEqual(ExchangeProposal.objects.get(pk=proposal.pk).status, 'accepted')
