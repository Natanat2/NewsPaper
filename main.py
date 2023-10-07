# Список команд для Django Shell

python manage.py shell
from news.models import *

# 1.Создать двух пользователей (с помощью метода User.objects.create_user('username')).
u1 = User.objects.create_user(username='Ivan')
u2 = User.objects.create_user(username='Sergey')

# 2.Создать два объекта модели Author, связанные с пользователями.
Author.objects.create(authorUser=u1)
Author.objects.create(authorUser=u2)

# 3.Добавить 4 категории в модель Category.
Category.objects.create(name='Sport')
Category.objects.create(name='IT')
Category.objects.create(name='Money')
Category.objects.create(name='Health')

# 4.Добавить 2 статьи и 1 новость.
aut = Author.objects.get(id=1)
Post.objects.create(author = aut, categoryType='AR', title='Статья 1', text='many words')
Post.objects.create(author = aut, categoryType='AR', title='Статья 2', text='too many words')
Post.objects.create(author = aut, categoryType='NW', title='Новость 1', text='words')

# 5.Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
Post.objects.get(id=1).Postcategory.add(Category.objects.get(id=1))
Post.objects.get(id=1).Postcategory.add(Category.objects.get(id=2))

# 6.Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть
# как минимум один комментарий).
Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=1).authorUser, text='good')
Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.objects.get(id=2).authorUser, text='yes')
Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=1).authorUser, text='good')
Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.objects.get(id=2).authorUser, text='u2')

# 7.Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
Post.objects.get(id=1).like()
Post.objects.get(id=2).like()
Comment.objects.get(id=1).like()
Comment.objects.get(id=1).dislike()
Comment.objects.get(id=1).dislike()

Post.objects.get(id=1).rating
Post.objects.get(id=2).rating
Comment.objects.get(id=1).rating

# 8.Обновить рейтинги пользователей.
a = Author.objects.get(id=1)
b = Author.objects.get(id=2)
a.update_rating()
b.update_rating()

# 9.Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
a = Author.objects.order_by('-ratingAuthor')[:-1]
for i in a:
    i.authorUser.username
    i.ratingAuthor

# 10.Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на
# лайках/дислайках к этой статье.
a = Post.objects.order_by('-rating')[:-1]
for i in a:
    i.dateCreation
    i.author.username
    i.rating
    i.title
    i.preview()

# 11.Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
a = Comment.objects.all
for i in a:
    i.dateCreation
    i.commentUser
    i.rating
    i.text