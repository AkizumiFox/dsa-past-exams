.PHONY: help clean FORCE   # vol1 等不能列為 PHONY，否則樣式規則不會套用

SHELL := /bin/bash
SRCDIR := src
BUILDDIR := build
OUTDIR := output
BUILD_TEXINPUTS := ../$(SRCDIR):../$(SRCDIR)/packages:
LATEXMK := latexmk -xelatex -cd- -output-directory=. -aux-directory=. -latexoption="-file-line-error -halt-on-error" -shell-escape -silent -interaction=nonstopmode

help:
	@echo "make vol1  - 產生並編譯第一冊（output/vol1.pdf）"
	@echo "make clean - 刪掉 build/"

vol%: FORCE
	@python3 scripts/assemble.py $*
	@mkdir -p $(BUILDDIR) $(OUTDIR)
	@cp $(SRCDIR)/vol$*.tex $(BUILDDIR)/vol$*.tex
	@TEXINPUTS="$(BUILD_TEXINPUTS)" scripts/build_tex.sh $(BUILDDIR) vol$*.tex $(LATEXMK)
	@cp $(BUILDDIR)/vol$*.pdf $(OUTDIR)/vol$*.pdf
	@echo "✓ $(OUTDIR)/vol$*.pdf"

clean:
	rm -rf $(BUILDDIR)

FORCE:
