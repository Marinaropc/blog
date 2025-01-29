from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def load_blog_posts():
    try:
        with open('storage.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_blog_posts(posts):
    with open('storage.json', 'w') as f:
        json.dump(posts, f, indent=4)


@app.route('/')
def index():
    blog_posts = load_blog_posts()
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_content = request.form.get('content')
        post_title = request.form.get('title')
        post_author = request.form.get('author')

        blog_posts = load_blog_posts()
        blog_posts.append({
            'id': len(blog_posts) + 1,
            'content': post_content,
            'title': post_title,
            'author': post_author
        })
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    blog_posts = load_blog_posts()
    update_posts= [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(update_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_blog_posts()
    post_to_update = next((post for post in blog_posts if post['id'] == post_id), None)
    if post_to_update is None:
        return "Post not found", 404
    if request.method == 'POST':
        post_to_update['content'] = request.form.get('content')
        post_to_update['title'] = request.form.get('title')
        post_to_update['author'] = request.form.get('author')
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post_to_update=post_to_update)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] += 1
            save_blog_posts(blog_posts)
            break
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)