class RenderCache:
    """Implements a rendering cache that stands in for an object
    having a method called render, and returning a pygame.Surface
    object.
    
    It wraps the rendering object and provides a forwarding method
    called render, which first asks the cache and then, if it has
    no entry for the arguments to the render method, forwards the
    request to the wrapped rendering object, intercepts the result,
    caches it, and returns it.
    
    It provides an end_frame method which deletes cached renders that
    have not been used during the last frame. The assumption is that
    the renders were cached for a certain number of frames, greater
    than 1, but once the value to be shown on the screen has changed,
    the old value will not be required again.
    
    It provides the hit count as the hits attribute, the miss count
    as the misses attribute, and the number of deleted cached renders
    as the deletions attribute.
    """

    def __init__(self, renderer):
        self.renderer = renderer
        self.renders = {}
        self.misses = 0
        self.hits = 0
        self.deletions = 0

    def render(self, *args):
        try:
            pair = self.renders[args]
            self.hits += 1
            pair[1] = True  # cached render, used this frame
            return pair[0]
        except KeyError:
            render = self.renderer.render(*args).convert_alpha()
            self.misses += 1
            self.renders[args] = [render, True]  # new render, used this frame
            return render

    def end_frame(self):
        new_renders = {}
        for key, value in self.renders.iteritems():
            if value[1]:
                new_renders[key] = [value[0], False]  # not used in next frame
        self.deletions += len(self.renders) - len(new_renders)
        self.renders = new_renders
