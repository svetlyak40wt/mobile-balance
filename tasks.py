from invoke import run, task

@task
def release():
    run('git push')
    run('git push --tags')
    run('python setup.py register')
    run('python setup.py sdist upload')
    run('python setup.py bdist_wheel upload')


@task
def serve_docs():
    from livereload import Server, shell

    build_command = 'sphinx-build -b html docs dist/docs'
    run(build_command)

    server = Server()
    server.watch('*.rst', shell(build_command))
    server.watch('docs/', shell(build_command))
    server.serve(root='dist/docs')