from pathlib import Path

from main import Post, Slide, photo_names, to_markdown


def slide(kind="info", photo=None):
    return Slide(kind=kind, title="T", text="", items=[], photo=photo, photo_query="")


post = Post(caption="Hook", hashtags=["prague", "#party"], slides=[slide("cover", 0), slide("facts", 7), slide("final", None)], notes=["Geotag"])
names = photo_names(post.slides, ["photo_0.jpg"], Path("."), "")
assert names == ["photo_0.jpg", None, None]

markdown = to_markdown(post, False, names)
assert "Hook\n\n#prague #party" in markdown and "- Geotag" in markdown and "2. facts: T (no photo)" in markdown
print("ok")
