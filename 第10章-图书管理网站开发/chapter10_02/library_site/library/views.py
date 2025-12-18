from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Book
from .forms import BookForm

# 硬编码的图书数据
BOOKS_DATA = [
    {
        'id': 1,
        'title': '活着',
        'author': '余华',
        'category': '文学',
        'description': '《活着》是作家余华的代表作之一，讲述了在大时代背景下，徐福贵的人生和家庭不断经受着苦难，到了最后所有亲人都先后离他而去，仅剩下年老的他和一头老牛相依为命。',
        'cover_image': '/static/library/images/book1.jpg'
    },
    {
        'id': 2,
        'title': '三体',
        'author': '刘慈欣',
        'category': '科幻',
        'description': '《三体》是刘慈欣创作的系列长篇科幻小说，讲述了地球人类文明和三体文明的信息交流、生死搏杀及两个文明在宇宙中的兴衰历程。',
        'cover_image': '/static/library/images/book2.jpg'
    },
    {
        'id': 3,
        'title': '百年孤独',
        'author': '加西亚·马尔克斯',
        'category': '文学',
        'description': '《百年孤独》是哥伦比亚作家加西亚·马尔克斯创作的长篇小说，是其代表作，也是拉丁美洲魔幻现实主义文学的代表作，被誉为"再现拉丁美洲历史社会图景的鸿篇巨著"。',
        'cover_image': '/static/library/images/book3.jpg'
    },
    {
        'id': 4,
        'title': '红楼梦',
        'author': '曹雪芹',
        'category': '古典文学',
        'description': '《红楼梦》是中国古代章回体长篇小说，中国古典四大名著之一。小说以贾、史、王、薛四大家族的兴衰为背景，以富贵公子贾宝玉为视角，描绘了一批举止见识出于须眉之上的闺阁佳人的人生百态。',
        'cover_image': '/static/library/images/book4.jpg'
    },
    {
        'id': 5,
        'title': '人类简史',
        'author': '尤瓦尔·赫拉利',
        'category': '历史',
        'description': '《人类简史》是以色列历史学家尤瓦尔·赫拉利的作品，从十万年前有生命迹象开始到21世纪资本、科技交织的人类发展史，将科学和历史编织在一起，从全新的角度阐述地球上智人的发展历程。',
        'cover_image': '/static/library/images/book5.jpg'
    },
    {
        'id': 6,
        'title': '小王子',
        'author': '安托万·德·圣-埃克苏佩里',
        'category': '童话',
        'description': '《小王子》是法国作家安托万·德·圣-埃克苏佩里于1943年写成的著名儿童文学短篇小说。本书的主人公是来自外星球的小王子。书中以一位飞行员作为故事叙述者，讲述了小王子从自己星球出发前往地球的过程中，所经历的各种历险。',
        'cover_image': '/static/library/images/book6.jpg'
    },
]

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 使用Django的认证系统
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('library:home')
        else:
            messages.error(request, '用户名或密码错误，请重试。')
    
    return render(request, 'library/login.html')

def home_view(request):
    # 检查用户是否已登录
    if not request.user.is_authenticated:
        return redirect('library:login')
    
    username = request.user.username
    books = Book.objects.all()
    context = {
        'username': username,
        'books': books
    }
    return render(request, 'library/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('library:login')

def add_book_view(request):
    if not request.user.is_authenticated:
        return redirect('library:login')
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '书籍添加成功！')
            return redirect('library:home')
        else:
            messages.error(request, '请检查输入的信息。')
    else:
        form = BookForm()
    
    return render(request, 'library/add_book.html', {'form': form})
