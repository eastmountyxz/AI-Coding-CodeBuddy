from django import forms
from .models import Book

# 定义可能的分类选项
CATEGORY_CHOICES = [
    ('文学', '文学'),
    ('科幻', '科幻'),
    ('古典文学', '古典文学'),
    ('历史', '历史'),
    ('童话', '童话'),
    ('推理', '推理'),
    ('技术', '技术'),
    ('艺术', '艺术'),
    ('哲学', '哲学'),
    ('其他', '其他'),
]

class BookForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label='分类')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cover_image': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '书名',
            'author': '作者',
            'description': '简介',
            'cover_image': '封面图片路径',
        }