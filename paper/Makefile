# Makefile for LaTeX paper compilation

# Main document
MAIN = main

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex

# Compilation flags
LATEXFLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean cleanall view

# Default target
all: $(MAIN).pdf

# Compile PDF
$(MAIN).pdf: $(MAIN).tex *.tex references.bib
	@echo "=== First LaTeX pass ==="
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	@echo ""
	@echo "=== Running BibTeX ==="
	$(BIBTEX) $(MAIN)
	@echo ""
	@echo "=== Second LaTeX pass ==="
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	@echo ""
	@echo "=== Third LaTeX pass ==="
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	@echo ""
	@echo "=== Compilation complete ==="
	@echo "Output: $(MAIN).pdf"

# Quick compile (no BibTeX)
quick: $(MAIN).tex
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex

# View PDF
view: $(MAIN).pdf
	xdg-open $(MAIN).pdf 2>/dev/null || open $(MAIN).pdf 2>/dev/null || echo "Please open $(MAIN).pdf manually"

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	@rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
	@echo "Clean complete"

# Clean everything including PDF
cleanall: clean
	@echo "Removing PDF..."
	@rm -f $(MAIN).pdf
	@echo "All files removed"

# Check for required packages
check:
	@echo "Checking LaTeX installation..."
	@which pdflatex > /dev/null && echo "✓ pdflatex found" || echo "✗ pdflatex not found"
	@which bibtex > /dev/null && echo "✓ bibtex found" || echo "✗ bibtex not found"
	@echo ""
	@echo "Checking for RevTeX 4-2..."
	@kpsewhich revtex4-2.cls > /dev/null && echo "✓ RevTeX 4-2 found" || echo "✗ RevTeX 4-2 not found (install with: tlmgr install revtex)"

# Word count (approximate)
wordcount:
	@echo "Approximate word count:"
	@detex $(MAIN).tex | wc -w

# Help
help:
	@echo "Makefile for LaTeX paper compilation"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Compile PDF with bibliography (default)"
	@echo "  quick     - Quick compile without bibliography"
	@echo "  view      - Open PDF in viewer"
	@echo "  clean     - Remove auxiliary files"
	@echo "  cleanall  - Remove all generated files including PDF"
	@echo "  check     - Check for required LaTeX packages"
	@echo "  wordcount - Approximate word count"
	@echo "  help      - Show this help message"
