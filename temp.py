from cement import App, Controller, ex


class Base(Controller):
    class Meta:
        label = 'base'
        stacked_on = 'base'
        stacked_type = 'nested'

    @ex(help='default action')
    def _default(self):
        print("Default action called!")
        self.another_method()

    def another_method(self):
        print("Another method within the same controller called!")


class MyApp(App):
    class Meta:
        label = 'myapp'
        base_controller = 'base'
        handlers = [
            Base
        ]


with MyApp() as app:
    app.run()
    
