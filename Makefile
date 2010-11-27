all: parse.out relatorio.pdf

parse.out: compilador.py testes/dummy.pas
	./compilador.py < testes/dummy.pas > /dev/null

relatorio.pdf: relatorio.tex
	pdflatex relatorio.tex

clean:
	rm parser.out parsetab.py parsetab.pyc relatorio.pdf relatorio.log