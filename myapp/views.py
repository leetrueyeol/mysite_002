from django.shortcuts import render, HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

nextid = 4
topics = [
  {'id':1, 'title':'routing', 'body':'Routing is ...'},
  {'id':2, 'title':'view', 'body':'View is ...'},
  {'id':3, 'title':'model', 'body':'Model is ...'},
]

# Create your views here.
# <li>routing</li>
# <li>views</li>
# <li>model</li>

def HTMLTemplate(articleTag, id = None):
  global topics
  contextUI = ''
  if id != None:
    contextUI = f''' 
    <li>
      <form action = "/delete/" method = "post">
        <input type = "hidden" name = "id" value = {id}>
        <input type = "submit" value = "delete">
      </form>
    </li>
    <li><a href="/update/{id}">update</a></li>
    '''
  ol = ''
  for topic in topics:  
    ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
  
  return f'''
    <html>
    <body>
      <h1><a href = "/">Django</a></h1>
      <ul>
        {ol}
      </ul>
      {articleTag}
      <ul>
        <li><a href = "/create/">create</a></li>
        {contextUI}
      </ul>  
    </body>    
    </html>
  '''

def index(request):
  article = '''
  <h2>Welcome to my Site</h2>
  <h3>Hello, Django Here is Start Position</h3>
  '''
  print("You are connected to the first page for the project , mysite_002.")
  # global topics
  # ol = ''
  # for topic in topics:
  #   # ol += f'<li>{topic["title"]}</li>'
    # ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
  # return HttpResponse('Welcome to my Site !')
  # return HttpResponse('<h1>Random</h1>' + str(random.random()))
        
  # return HttpResponse(f'''
  #   <html>
  #   <body>
  #     <h1>Django</hi>
  #     <ol>
  #       {ol}
  #     </ol>
  #     <h2>Welcome to my Site</h2>
  #     Hello,  Django
  #   </body>
  #   </html>
  #   ''')
  return HttpResponse(HTMLTemplate(article))

@csrf_exempt
def create(request):
  global nextid
  print('request.method --> ', request.method)
  if request.method == 'GET':
    article = '''
      <form action = "/create/" method = "Post">
        <p><input type = "text" name = "title" placeholder = "title"></p>
        <p><textarea name = "body" placeholder = "body"></textarea></p>
        <p><input type = "submit"></p>
      </form>
      '''
    return HttpResponse(HTMLTemplate(article))
  elif request.method == 'POST':
    print('')
    print('request.method --> ', request.method)
    print('')
    title = request.POST['title']
    body = request.POST['body']
    newTopic = {"id":nextid, "title":title, "body":body}
    url = '/read/' + str(nextid)
    nextid = nextid + 1
    topics.append(newTopic)
    # return HttpResponse('')
    # return HttpResponse(request.POST['title'])
    # return HttpResponse(HTMLTemplate('whatever'))
    return redirect(url)
  
  # return HttpResponse('creating a new Web page !')
# def read(request):
#   return HttpResponse('reading a new Web page !')

@csrf_exempt
def update(request, id):
  global topics
  if request.method == 'GET':
    for topic in topics:
      if topic['id'] == int(id):
        selectedTopic = {"title":topic['title'], "body":topic['body']}
    # article = 'Update'
    article = f'''
      <form action = "/update/{id}/" method = "post">
        <p><input type = "text" name = "title" placeholder = "title" value = {selectedTopic["title"]}></p>
        <p><textarea name = "body" placeholder = "body">{selectedTopic['body']}</textarea></p>
        <p><input type = "submit"></p>
      </form>
      '''
    return HttpResponse(HTMLTemplate(article, id))

  elif request.method == 'POST':
    title = request.POST['title']
    body = request.POST['body']
    for topic in topics:
      if topic['id'] == int(id):
        topic['title'] = title
        topic['body'] = body
    return redirect(f'/read/{id}')


@csrf_exempt
def delete(request):
  global topics
  if request.method == 'POST':
    id = request.POST['id']
    print('')
    print('id --> ', id)
    print('')
    newTopics = []
    for topic in topics:
      if topic['id'] != int(id):
        newTopics.append(topic)
    topics = newTopics
        
    return redirect('/')

def read(request, id):
  global topics
  article = ''
  print('')
  for topic in topics:
    # print("type in in topic['id'] --> ", type(topic['id']), "id type in arg --> ",type(id))
    print('id in read -->', topic['id'])
    if topic['id'] == int(id):
      article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
  print('')
  # return HttpResponse('reading a new Web page !  ' + id)
  return HttpResponse(HTMLTemplate(article, id))
