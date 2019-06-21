FC = gfortran
FFLAGS = -Ofast -std=legacy -fno-stack-protector

SRC_FILES = mkp_wrapper.f90 MTM.FOR

all:
	$(FC) $(FFLAGS) $(SRC_FILES) -o mkp_wrapper

clean:
	rm -f mkp_wrapper
