from flask import Flask, render_template, request, redirect, url_for
import docker

app = Flask(__name__)
client = docker.from_env()


@app.route('/')
def index():
    containers = client.containers.list(all=True)
    images = [image.tags[0] for image in client.images.list()]
    return render_template('index.html', containers=containers, images=images)

@app.route('/start/<id>')
def start_container(id):
    container = client.containers.get(id)
    container.start()
    return redirect(url_for('index'))

@app.route('/stop/<id>')
def stop_container(id):
    container = client.containers.get(id)
    container.stop()
    return redirect(url_for('index'))

@app.route('/create', methods=['POST'])
def create_container():
    image = request.form['image']
    name = request.form['name']
    port = request.form['port']
    container = client.containers.create(
        image=image,
        name=name,
        ports={'80/tcp': port},
        detach=True
    )
    container.start()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete_container(id):
    container = client.containers.get(id)
    container.stop()
    container.remove()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

