from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import stripe
from decimal import Decimal
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import *
from .models import NFT

from django.shortcuts import render, get_object_or_404, redirect
from .models import NFT, Transaction 
import stripe
from django.conf import settings
import requests

from .forms import (
    RegistrationForm,
    PostForm,
    CommentForm,
    NewsCommentForm,
    FeedbackRatingForm,
    BuyStockForm,
    SellStockForm,
    CurrencyConverterForm,
    NFTForm,
    GlossaryTermForm,
)

from .forms import (
    CustomAuthenticationForm,
    RegistrationForm,
    PostForm,
    CommentForm,
    NewsCommentForm,
    SellStockForm, SellNFTForm,
)
from .models import (
    Transaction,
    UserHolding,
    User,
    Learn,
    CourseCategory,
    Feedback,
    News,
    Post,
    Comment,
    Stock,
    NFT,
    Bid,
    GlossaryTerm,
)

stripe.api_key = settings.STRIPE_PRIVATE_KEY


# Create your views here.


def home(request):
    stocks = Stock.objects.all()
    return render(request, "index.html", {"stocks": stocks})


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"


def register(request):
    context = {"form": "", "errors": ""}
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            hashed_password = make_password(cleaned_data["password"])
            cleaned_data["password"] = hashed_password
            form.cleaned_data = cleaned_data
            user = form.save()
            login(request, user)

            # Redirect to the home page after registration
            return redirect("home")

        context["errors"] = form.errors
        context["form"] = form
    else:
        form = RegistrationForm()
        context["form"] = form
    return render(request, "registration/register.html", context)


def news(request):
    context = {"title": "Latest Crypto News", "news": News.objects.all()}
    return render(request, "News/index.html", context)


@login_required(login_url="/login/")
def transaction_history(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by("-timestamp")

    items_per_page = 10
    paginator = Paginator(transactions, items_per_page)
    page = request.GET.get('page')

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(
        request, "transaction/transaction_history.html", {
            "transactions": transactions}
    )


def categories_course(request):
    categories = CourseCategory.objects.all()
    return render(request, "Learn/learning.html", {"categories": categories})


def subject_info(request, slug):
    subject = get_object_or_404(Learn, slug=slug)
    description = subject.description
    return render(
        request,
        "Learn/learning-details.html",
        {"subject": subject, "description": description},
    )


def submit_feedback(request, sub_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            feedbacks = Feedback.objects.get(
                user__id=request.user.id, topic__id=sub_id)
            form = FeedbackRatingForm(request.POST, instance=feedbacks)
            form.save()
            messages.success(
                request, "Thank you! Your feedback has been updated.")
            return redirect(url)
        except Feedback.DoesNotExist:
            form = FeedbackRatingForm(request.POST)
            if form.is_valid():
                data = Feedback()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.feedback = form.cleaned_data["feedback"]
                data.ip = request.META.get("REMOTE_ADDR")  # Change this line
                data.topic_id = sub_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, "Thank you! Your feedback has been submitted."
                )
                return redirect(url)


def discussion(request):
    ord_by = request.GET.get("order_by")
    order_string = "-views"
    if ord_by == None or ord_by == "max-views" or ord_by == "":
        order_string = "-views"
    elif ord_by == "min-views":
        order_string = "views"
    elif ord_by == "latest":
        order_string = "-created_at"
    elif ord_by == "oldest":
        order_string = "created_at"

    post_list = Post.objects.all().order_by(
        order_string
    )  # Replace with your queryset for your posts
    paginator = Paginator(post_list, 2)  # Show 5 posts per page
    page = request.GET.get("page")
    posts = paginator.get_page(page)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user  # Assign the logged-in user
            post.save()
            return redirect("discussion")
    else:
        form = PostForm()
    return render(request, "posts/discussion_all.html", {"posts": posts, "form": form})


def discussion_single(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.all().order_by("-created_at")

    # Add pagination for comments (e.g., 5 comments per page)
    paginator = Paginator(comments, 1)
    page = request.GET.get("page")
    comments_page = paginator.get_page(page)

    if request.method == "GET" and page == None and request.GET.get("fl") != None:
        post.views += 1
        post.save()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_by = request.user
            comment.save()
            return redirect("discussion_single", post_id=post_id)

    else:
        form = CommentForm()

    return render(
        request,
        "posts/discussion_single.html",
        {"post": post, "comments": comments_page, "form": form},
    )


def show_stocks(request):
    stocks = Stock.objects.all()
    return render(request, "Stocks/showStocks.html", {"stocks": stocks})


@login_required(login_url="/login/")
def buy_stock(request, stock_symbol):
    error_message = ""
    stock = get_object_or_404(Stock, symbol=stock_symbol)

    if request.method == 'POST':
        form = BuyStockForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            total_price = stock.current_price * quantity  # Calculate total price

            # Handle Stripe payment
            token = form.cleaned_data["stripeToken"]
            try:
                charge = stripe.Charge.create(
                    amount=int(total_price * 100),  # Amount in cents
                    currency="cad",
                    source=token,
                    description=f"Stock Purchase: {stock_symbol}",
                )

                # Record the transaction
                transaction = Transaction(
                    user=request.user,
                    asset=stock,  # Use the generic asset field
                    transaction_type="Buy",
                    quantity=quantity,
                    price=total_price,
                )
                transaction.save()

                # Update user holdings
                holding, created = UserHolding.objects.get_or_create(
                    user=request.user, content_type=ContentType.objects.get_for_model(stock), object_id=stock.id
                )
                holding.quantity += quantity
                holding.save()

                return redirect("transaction-history")
            except stripe.error.CardError as e:
                error_message = e.error.message
                print(f"Stripe CardError: {error_message}")
    else:
        form = BuyStockForm()

    return render(
        request,
        "Stocks/buy_stock.html",
        {
            "stock": stock,
            "error_message": error_message,
            "PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "form": form,
        },
    )


@login_required(login_url="/login/")
def user_holdings(request):
    holdings = UserHolding.objects.filter(user=request.user)
    sell_stock_form = SellStockForm()
    sell_nft_form = SellNFTForm()
    items_per_page = 10
    paginator = Paginator(holdings, items_per_page)
    page = request.GET.get('page')

    try:
        holdings_page = paginator.page(page)
    except PageNotAnInteger:
        holdings_page = paginator.page(1)
    except EmptyPage:
        holdings_page = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if 'sell_stock' in request.POST:
            sell_stock_form = SellStockForm(request.POST)
            if sell_stock_form.is_valid():
                stock_symbol = sell_stock_form.cleaned_data['stock_symbol']
                quantity_to_sell = sell_stock_form.cleaned_data['quantity']
                stock = Stock.objects.get(symbol=stock_symbol)
                holding = holdings.filter(stock=stock).first()
                if holding and quantity_to_sell > 0 and quantity_to_sell <= holding.quantity:
                    sell_price = stock.current_price * quantity_to_sell

                    sell_transaction = Transaction(
                        user=request.user,
                        stock=stock,
                        transaction_type="Sell",
                        quantity=quantity_to_sell,
                        price=sell_price,
                    )
                    sell_transaction.save()
                    holding.quantity -= quantity_to_sell
                    holding.save()
                    request.user.wallet += Decimal(sell_price)
                    request.user.save()
                    if holding.quantity == 0:
                        holding.delete()

                    return redirect("user-holdings")
                else:
                    error_message = 'Invalid quantity to sell. Please select a valid quantity.'
                    sell_stock_form.add_error('quantity', error_message)

        elif 'sell_nft' in request.POST:
            sell_nft_form = SellNFTForm(request.POST)
            if sell_nft_form.is_valid():
                nft_symbol = sell_nft_form.cleaned_data['nft_symbol']
                quantity_to_sell = sell_nft_form.cleaned_data['quantity']
                nft = NFT.objects.get(symbol=nft_symbol)
                holding = holdings.filter(nft=nft).first()
                if holding and quantity_to_sell > 0 and quantity_to_sell <= holding.quantity:
                    sell_price = nft.current_price * quantity_to_sell

                    sell_transaction = Transaction(
                        user=request.user,
                        nft=nft,
                        transaction_type="Sell",
                        quantity=quantity_to_sell,
                        price=sell_price,
                    )
                    sell_transaction.save()
                    holding.quantity -= quantity_to_sell
                    holding.save()
                    request.user.wallet += Decimal(sell_price)
                    request.user.save()
                    if holding.quantity == 0:
                        holding.delete()

                    return redirect("user-holdings")

                else:
                    error_message = 'Invalid quantity to sell. Please select a valid quantity.'
                    sell_nft_form.add_error('quantity', error_message)

    return render(request, 'userholding/user_holdings.html',
                  {'user': request.user, 'holdings': holdings_page, 'sell_stock_form': sell_stock_form, 'sell_nft_form': sell_nft_form})

def newsDetails(request, news_id):
    if request.method == "POST":
        comment = NewsCommentForm(request.POST)

    newsDetails = get_object_or_404(News, pk=news_id)
    form = NewsCommentForm()
    return render(
        request, "NewsDetails/index.html", {"news": newsDetails, "form": form}
    )


def nftmarketplace(request):
    nfts = NFT.objects.all()
    return render(request, "Nft/NFTmarketplace.html", {"nfts": nfts})


def nft_detail(request, nft_id):
    nft = get_object_or_404(NFT, pk=nft_id)
    return render(request, "nft/NFT.html", {"nft": nft})

def create_nft(request):
    if request.method == 'POST':
        form = NFTForm(request.POST, request.FILES)
        if form.is_valid():
            nft_instance = form.save(commit=False)
            
            # Check if the user is authenticated (logged in)
            if request.user.is_authenticated:
                nft_instance.owner = request.user
                nft_instance.save()
                return redirect('nft_detail', nft_id=nft_instance.id)
            else:
                # Handle the case when the user is not logged in (redirect to login page, for example)
                return redirect('login')  # Replace 'login' with the actual login URL

    else:
        form = NFTForm()

    return render(request, 'nft/create_nft.html', {'form': form})

# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required  # Import login_required
from .models import NFT, Transaction, UserHolding
from .forms import BuyNFTForm
import stripe
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


# Updated buy_nft view
@login_required(login_url="/login/")
def buy_nft(request, nft_id):
    error_message = ""
    nft = get_object_or_404(NFT, id=nft_id)

    if request.method == 'POST':
        form = BuyNFTForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            total_price = nft.current_price * quantity  # Calculate total price

            # Handle Stripe payment
            token = form.cleaned_data["stripeToken"]
            try:
                charge = stripe.Charge.create(
                    amount=int(total_price * 100),  # Amount in cents
                    currency="usd",  # Adjust currency based on your needs
                    source=token,
                    description=f"NFT Purchase: {nft.symbol}",
                    )
                # Record the transaction
                transaction = Transaction(
                    user=request.user,
                    nft=nft,
                    transaction_type="Buy",
                    quantity=quantity,
                    price=total_price,
                )
                transaction.save()
                # Example: Update UserHolding
                holding, created = UserHolding.objects.get_or_create(user=request.user, nft=nft)
                holding.quantity += form.cleaned_data['quantity']
                holding.save()

                # Redirect to user holdings or a success page
                return redirect("user-holdings") # Adjust the URL based on your configuration
            except stripe.error.CardError as e:
                error_message = e.error.message
                print(f"Stripe CardError: {error_message}")
    else:
        form = BuyNFTForm()

    return render(
        request,
        "Nft/buy_nft.html",  # Adjust the template path based on your app structure
        {
            "nft": nft,
            "error_message": error_message,
            "PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "form": form,
        },
    )

def cryptocurrency_data(request):
    # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/map'
    # url = 'https://sandbox-api.coinmarketcap.com/v1/fiat/map'
    parameters = {"limit": 10}
    headers = {
        "Accepts": "application/json",
        # 'X-CMC_PRO_API_KEY': '6f66fcc3-73b3-48ea-a584-32af97de8e12',
        "X-CMC_PRO_API_KEY": "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c",
    }

    try:
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()
        return render(request, "test_template.html", {"data": data})
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects,
    ) as e:
        return render(request, "test_template.html", {"error_message": str(e)})


def convert(source,to,amount):

    # url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    # url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/map'

    url = 'https://sandbox-api.coinmarketcap.com/v2/tools/price-conversion'
    parameters = {
        'id':source,
        'convert_id':to,
        'amount':amount
    }

    headers = {
        "Accepts": "application/json",
        # 'X-CMC_PRO_API_KEY': '6f66fcc3-73b3-48ea-a584-32af97de8e12',
        "X-CMC_PRO_API_KEY": "b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c",
    }

    try:
        response = requests.get(url, params=parameters, headers=headers)
        print(data)
        return data['data'][to]['quote'][to]['price']

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as e:
        return render(request, 'test_template.html', {'error_message': str(e)})

def convert_data(request):
    result = None

    # Example choices (you can replace this with actual currency choices)
    currency_choices = [(2781, 'BTC'), (2784, 'EUR'), (3, 'GBP')]

    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        form.set_currency_choices(currency_choices)
        if form.is_valid():
            result=convert(form.cleaned_data['currency_from'],form.cleaned_data['currency_to'],form.cleaned_data['amount'])
        return render(request, 'test_template.html', {'form': form, 'result': result})


    else:
        form = CurrencyConverterForm()
        form.set_currency_choices(currency_choices)

    return render(request, 'test_template.html', {'form': form, 'result': result})


def glossary(request):
    # Retrieve all glossary terms ordered alphabetically
    terms = GlossaryTerm.objects.order_by('term')
    
    return render(request, 'Glossary/Terms.html', {'terms': terms})

def term_detail(request, term_id):
    # Retrieve the detailed information for a specific term
    term = get_object_or_404(GlossaryTerm, id=term_id)
    
    return render(request, 'Glossary/Terms_details.html', {'term': term})