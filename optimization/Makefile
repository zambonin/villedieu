FC = gfortran
FFLAGS = -Ofast -std=legacy -fno-stack-protector

TARGET_F = mkp_wrapper
SRC_F_FILES = $(TARGET_F).f90 MTM.FOR
SRC_TEX_FILES = $(wildcard docs/*.tex)

all: docs mkp

%.pdf: %.tex
	latexmk -interaction=nonstopmode -shell-escape -pdf -use-make -cd $<

docs: $(SRC_TEX_FILES:.tex=.pdf)

mkp: $(SRC_F_FILES)
	$(FC) $(FFLAGS) $^ -o $(TARGET_F)

clean:
	$(RM) $(TARGET_F)
	latexmk -cd -C $(SRC_TEX_FILES)
