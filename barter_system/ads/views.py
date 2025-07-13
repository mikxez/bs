from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def ad_list(request):
    ads = Ad.objects.all()
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if query:
        ads = ads.filter(title__icontains=query) | ads.filter(description__icontains=query)
    if category:
        ads = ads.filter(category__iexact=category)
    if condition:
        ads = ads.filter(condition__iexact=condition)

    paginator = Paginator(ads.order_by('-created_at'), 1)
    page = request.GET.get('page')
    ads = paginator.get_page(page)
    return render(request, 'ads/ad_list.html', {'ads': ads})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})

@login_required
def proposal_create(request):
    receiver_id = request.GET.get('receiver')
    initial_data = {}
    if receiver_id:
        try:
            receiver_ad = Ad.objects.get(pk=receiver_id)
            if receiver_ad.user != request.user:
                initial_data['ad_receiver'] = receiver_ad
        except:
            pass

    if request.method == 'POST':
        form = ProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.status = 'pending'
            proposal.save()
            return redirect('proposal_list')
    else:
        form = ProposalForm(user=request.user, initial=initial_data)

    return render(request, 'ads/proposal_form.html', {'form': form})



@login_required
def proposal_update_status(request, pk, status):
    proposal = get_object_or_404(ExchangeProposal, pk=pk)
    if proposal.ad_receiver.user != request.user:
        return HttpResponseForbidden()
    if status in ['accepted', 'rejected']:
        proposal.status = status
        proposal.save()
    return redirect('proposal_list')

@login_required
def proposal_list(request):
    proposals = ExchangeProposal.objects.all()
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    status = request.GET.get('status')

    if sender:
        proposals = proposals.filter(ad_sender__user__username__iexact=sender)
    if receiver:
        proposals = proposals.filter(ad_receiver__user__username__iexact=receiver)
    if status:
        proposals = proposals.filter(status__iexact=status)

    return render(request, 'ads/proposal_list.html', {'proposals': proposals})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('ad_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ad_list')
    else:
        form = AuthenticationForm()
    return render(request, 'ads/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('ad_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ad_list')
    else:
        form = UserCreationForm()
    return render(request, 'ads/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
