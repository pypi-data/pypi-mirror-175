#!/usr/bin/make -f
# Makefile for QJackCapture #
# ------------------------- #

PREFIX ?= /usr/local
DESTDIR ?= /

INSTALL ?= install
PYTHON ?= python3
PYUIC ?= pyuic5
PYRCC ?= pyrcc5
PYPKG = qjackcapture
PROGRAM = qjackcapture
TWINE ?= twine
ICON = resources/icons/48x48/$(PROGRAM).png
DESKTOP_FILE = resources/xdg/$(PROGRAM).desktop

# -------------------------------------------------------------------------------------------------

all: RES UI

# -------------------------------------------------------------------------------------------------
# Resources

RES: $(PYPKG)/resources_rc.py

$(PYPKG)/resources_rc.py: resources/resources.qrc
	$(PYRCC) $< -o $@

# -------------------------------------------------------------------------------------------------
# UI code

UI: qjackcapture

qjackcapture: $(PYPKG)/ui_mainwindow.py \
	$(PYPKG)/app.py \
	$(PYPKG)/__main__.py \
	$(PYPKG)/version.py

$(PYPKG)/ui_%.py: resources/ui/%.ui
	$(PYUIC) --from-imports -o $@ $<

# -------------------------------------------------------------------------------------------------

clean:
	-rm -f *~ $(PYPKG)/*~ $(PYPKG)/*.pyc $(PYPKG)/ui_*.py $(PYPKG)/*_rc.py

# -------------------------------------------------------------------------------------------------

install-data:
	$(INSTALL) -dm755  $(DESTDIR:/=)$(PREFIX)/share/icons/hicolor/48x48/apps
	$(INSTALL) -m644 $(ICON) $(DESTDIR:/=)$(PREFIX)/share/icons/hicolor/48x48/apps
	$(INSTALL) -dm755 $(DESTDIR:/=)$(PREFIX)/share/applications
	$(INSTALL) -m644 $(DESKTOP_FILE) $(DESTDIR:/=)$(PREFIX)/share/applications
	@if [ -z "$(DESTDIR)" ]; then \
		echo "Updating desktop menu..."; \
		update-desktop-database -q; \
	fi
	@if [ -z "$(DESTDIR)" ]; then \
		echo "Updating icon cache..."; \
		gtk-update-icon-cache -q $(DESTDIR:/=)$(PREFIX)/share/icons/hicolor; \
	fi

install: install-data
	$(PYTHON) setup.py install --prefix=$(PREFIX) --root=$(DESTDIR)

install-pip: install-data
	$(PYTHON) -m pip install --prefix=$(PREFIX) --root=$(DESTDIR) .

# -------------------------------------------------------------------------------------------------

uninstall:
	$(PYTHON) -m pip uninstall $(PYPKG)

# -------------------------------------------------------------------------------------------------

dist: sdist wheel

sdist: RES UI
	$(PYTHON) -m build --sdist

wheel: RES UI
	$(PYTHON) -m build --wheel

release: sdist wheel

pypi-upload: release
	$(TWINE) upload --skip-existing dist/*.tar.gz dist/*.whl


.PHONY: all dist install install-data install-pip pypi-upload release sdist uninstall wheel
