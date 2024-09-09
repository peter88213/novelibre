"""Create a German translation."""
import build

ab = build.ApplicationBuilder(build.VERSION)
ab.build_script()
ab.build_translation()
ab.clean_up()

