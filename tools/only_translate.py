"""Create a German translation."""
import build

ab = build.ApplicationBuilder(build.VERSION)
ab.build_py_module()
ab.build_translation()
ab.clean_up()

