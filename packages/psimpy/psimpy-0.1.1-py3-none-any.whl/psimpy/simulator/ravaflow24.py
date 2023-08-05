import os
import linecache
import numpy as np
from scipy.interpolate import interp2d
from typing import Union
from beartype import beartype

class Ravaflow24Mixture:
    
    @beartype
    def __init__(
        self, dir_sim: str, time_step: Union[float, int] = 10,
        time_end: Union[float, int] = 300, cfl: float = 0.4, 
        time_step_length: float = 0.001, conversion_control: str = '0',
        curvature_control: str = '1', surface_control: str = '0',
        entrainment_control: str = '0', shear_velocity_coef: float = 0.05,
        basal_friction_diff: float = 0.0, stopping_control: str = '0',
        stopping_threshold: float = 0.0, friction_control: str = '0') -> None:
        """
        A wrapper for the Voellmy-type shallow flow model of r.avaflow 2.4.

        Parameters
        ----------
        dir_sim : str
            Main directory to save simulation outputs.
        time_step : float or int
            Time step for simulation, in seconds.
        time_end : float or int
            End time for simulation, in seconds.
        cfl : float
            CFL criterion, a value being equal or smaller than 0.5.
        time_step_length : float
            If CFL criterion is not applicable, `time_step_length` is used.
            In seconds. Recommended range is around 0.1 to 0.5.
        conversion_control : str
            If '0', no conversion of flow heights to flow depths.
            If '1', conversion is applied.
        curvature_control : str
            If '0', curvature is neglected.
            If '1', curvature is considered in the decelerating source terms.
            If '2', curvature is considered in all relevant terms.
        surface_control : str
            If '0', no balancing of forces.
            If '1', apply balancing of forces.
        entrainment_control : str
            If '0', no entrainment.
            If '1', the entrainment coefficient is multiplied with flow momentum.
            If '2', simplified entrainment and deposition model is used.
            If '3', combination of '1' for entrainmnet and '2' for deposition.
            If '4', acceleration-deceleration entrainment and deposition model.
        shear_velocity_coef : float
            Only used with entrainment_control being '2' or '3', range [0,1]
        basal_friction_diff : float
            Difference between the basal friction angles of the basal surface
            and the flow, in degrees. Only used with entrainment_control being
            '2' or '3'.
        stopping_control : str
            If '0', no stopping control is used.
            If '1', stop if the flow kinetic energy is equal or smaller than a
            given threshold.
            If '2', stop if the flow momentum is equal or smaller than a given
            threshold.
            If '3', stop if the dynamic flow pressure of all raster cells is
            euqal or smaller than a given threshold.
        stopping_threshold : float
            Threshold value for stopping_control.
            If stopping_control is '1' or '2', stopping_threshold has to be
            given as the maximum value reached during the flow.
            If stopping_control is '3', the pressure threshold has to be
            specified.
        friction_control : str, optional
            If '0', no dynamic adaptation of friction parameters.
            If '1', dynamic adaptation of friction parameters (ignored for the
            mixture model).
        
        """
        if not os.path.isdir(dir_sim):
            raise ValueError(f"{dir_sim} does not exist or is not a directory")
        self.dir_sim = dir_sim

        self.time_step = time_step
        self.time_end = time_end
        self.cfl = cfl
        self.time_step_length = time_step_length
        
        if conversion_control not in ['0','1']:
            raise ValueError("convresion_control must be '0' or '1'")
        self.conversion_control = conversion_control
        
        if curvature_control not in ['0','1','2']:
            raise ValueError("curvature_control must be '0' or '1' or '2'")
        self.curvature_control = curvature_control 
        
        if surface_control not in ['0','1']:
            raise ValueError("surface_control must be '0' or '1'")
        self.surface_control = surface_control
        
        if entrainment_control not in ['0','1','2','3','4']:
            raise ValueError(
                "entrainment_control must be '0', '1', '2', '3', or '4'")
        self.entrainment_control = entrainment_control
        
        self.shear_velocity_coef = shear_velocity_coef
        self.basal_friction_diff = basal_friction_diff
        
        if stopping_control not in ['0','1','2','3']:
            raise ValueError("stopping_control must be '0', '1', '2', or '3'")
        self.stopping_control = stopping_control
                 
        self.stopping_threshold = stopping_threshold

        if friction_control not in ['0','1']:
            raise ValueError("friction_control must be '0' or '1'")
        self.friction_control = friction_control
    
    @beartype
    def preprocess(
        self, prefix: str, elevation: str, hrelease: str,
        cellsize: Union[float, int, np.floating, np.integer] = 20,
        hrelease_ratio: Union[float, np.integer] = 1.0, 
        internal_friction: Union[float, int, np.floating, np.integer] = 35,
        basal_friction: Union[float, int, np.floating, np.integer] = 20,
        turbulent_friction: Union[float, int, np.floating, np.integer] = 3,
        entrainment_coef: Union[float, np.floating] = -7.0,
        EPSG: Union[str, None] = None) -> tuple[str, str]:
        """
        Preprocess simulation input data.

        Parameters
        ----------
        prefix : str
            Prefix to name output files.
        elevation : str
            Name of elevation raster file (including its path).
            The file format should be supported by GDAL.
            Its unit is in meters.
        hrelease : str
            Name of release height raster file (including its path).
            The file format should be supported by GDAL.
            Its unit is in meters.
        cellsize : float or int, optional
            Cell size in meters to be used in simulation.
        hrelease_ratio : float, optional
            A positive float value to multiple the hrelease in order to control
            the release volume.
        internal_friction : float or int, optional
            Internal friction angle, in degrees, range [0,90).
        basal_friction : float or int, optional
            Basal friction angle, in degrees, range [0,90).
        turbulent_friction : float or int, optional
            Logarithm with base 10 of the turbulent friction, in m/s^2.
        entrainment_coef : float, optional
            Logarithm with base 10 of the entrainment coefficient, except for 0
            meaning no entrainment.
        EPSG : str, optional
            EPSG (European Petroleum Survey Group) code to create grass location.
            If None, `elevation` must be a georeferenced file which has metadata
            to create the grass location. 
        
        Returns
        -------
        grass_location : str
            Name of the GRASS LOCATION (including path).
        sh_file : str
            Name of the shell file (including path), which will be called by
            GRASS to run the simulation. 
        """        
        sh_file = os.path.join(self.dir_sim, f'{prefix}_shell.sh')
        grass_location = os.path.join(self.dir_sim, f'{prefix}_glocation')
        results_dir = os.path.join(self.dir_sim, f'{prefix}_results')

        if os.path.exists(sh_file) or os.path.exists(grass_location) or \
            os.path.exists(results_dir):
            raise ValueError(
                f"File(s) with prefix={prefix} already exists in {self.dir_sim}."
                f" Move or delete conflicting files, or use another prefix.")
        
        if not os.path.exists(elevation):
            raise ValueError(f"{elevation} does not exist")
        
        if not os.path.exists(hrelease):
            raise ValueError(f"{hrelease} does not exist")
        
        # create grass location
        if EPSG is None:
            os.system(f"grass -e -c {elevation} {grass_location}")
        else:
            os.system(f"grass -e -c EPSG:{EPSG} {grass_location}")

        # create shell file
        with open(sh_file, 'w') as sh:

            sh.write("# import elevation raster \n")
            sh.write(f"r.in.gdal -o input={elevation} output=elev --overwrite")
            sh.write("\n\n")

            sh.write("# set region based on elev \n")
            sh.write("g.region raster=elev \n\n")
            
            sh.write('# import hrelease raster \n')
            sh.write(
                f"r.in.gdal -o input={hrelease} output=raw_hrel --overwrite")
            sh.write("\n\n")

            sh.write(
                f"r.mapcalc \"hrel = raw_hrel*{hrelease_ratio}\" --overwrite")
            sh.write("\n\n")
            
            sh.write(
                f"r.avaflow -e -a prefix={prefix} cellsize={cellsize} phases=x "
                f"elevation=elev hrelease=hrel "
                f"friction={internal_friction},{basal_friction},"
                f"{turbulent_friction} "
                f"basal={entrainment_coef},{self.shear_velocity_coef},"
                f"{self.basal_friction_diff},{self.stopping_threshold} "
                f"controls={self.conversion_control},{self.curvature_control},"
                f"{self.surface_control},{self.entrainment_control},"
                f"{self.stopping_control},{self.friction_control} "
                f"time={self.time_step},{self.time_end} "
                f"cfl={self.cfl},{self.time_step_length}")
        
        return grass_location, sh_file

    @beartype
    def run(self, grass_location: str, sh_file: str) -> None:
        """
        Parameters
        ----------
        grass_location : str
            Name of the GRASS LOCATION (including path).
        sh_file : str
            Name of the shell file (including path).
        """
        if not os.path.exists(grass_location):
            raise ValueError(f"{grass_location} does not exist")
        if not os.path.exists(os.path.join(grass_location, "PERMANENT")):
            raise ValueError(f"{grass_location} is not a grass location")
        
        if not os.path.exists(sh_file):
            raise ValueError(f"{sh_file} does not exist")
        
        grass_mapset = os.path.join(grass_location, "PERMANENT", "")

        os.chdir(self.dir_sim)
        os.system(f"grass {grass_mapset} --exec sh {sh_file}")


    def extract_impact_area(self, prefix: str, qoi: str = 'h',
        threshold: Union[float, int] = 0.5) -> float:
        """
        Extract impact area defined by a given quantity of interest (qoi) and
        its threshold.

        Parameters
        ----------
        prefix : str
            Prefix used to name output files.
        qoi : str
            qoi to determine the impact area.
            'h' - maximum flow height, in meters
            'v' - maximum flow velocity, in m/s
            'p' - maximum flow pressure, in Pa
            't' - maximum flow kinetic energy, in J
        threshold : float or int
            Areas where `qoi` is larger than the threshold are regarded as 
            impar area.

        Returns
        -------
        impact_area : float
            A scalar value representing the overall impact area.
        """
        if qoi not in ['h','v','p','t']:
            raise ValueError("qoi must be 'h', 'v', 'p', or 't'")

        qoi_max_raster_asc = os.path.join(self.dir_sim, f'{prefix}_results',
            f'{prefix}_ascii', f'{prefix}_{qoi}flow_max.asc')
        qoi_max_raster = np.loadtxt(qoi_max_raster_asc, skiprows=6)

        cellsize = linecache.getline(qoi_max_raster_asc, 5)
        cellsize = float(cellsize.split()[-1].strip())

        impact_area = np.sum(np.where(qoi_max_raster>threshold,1,0)) * \
            (cellsize)**2
            
        return float(impact_area)

    def extract_qoi_max(self, prefix: str, qoi: str,
        aggregate: bool = True) -> Union[float, np.ndarray]:
        """
        Extract the maximum value(s) of a quantity of interest (qoi) in one 
        simulation.
        
        Parameters
        ----------
        prefix : str
            Prefix used to name output files.
        qoi : str
            Quantity of interest.
            'h' - maximum flow height, in meters
            'v' - maximum flow velocity, in m/s
            'p' - maximum flow pressure, in Pa
            't' - maximum flow kinetic energy, in J
        aggregate : bool
            If True, returns the overall maximum value over all spatio-tempo
            grids.
            If False, returns the maximum values over all time steps at each
            spatio location, namely a raster of maximum values at location.

        Returns
        -------
        qoi_max : float or numpy array
            Maximum value(s) of qoi in one simulation.
            
        """
        if qoi not in ['h','v','p','t']:
            raise ValueError("qoi must be 'h', 'v', 'p', or 't'")
        
        qoi_max_raster_asc = os.path.join(self.dir_sim, f'{prefix}_results',
            f'{prefix}_ascii', f'{prefix}_{qoi}flow_max.asc')
        qoi_max_raster = np.loadtxt(qoi_max_raster_asc, skiprows=6)

        if aggregate:
            return float(np.max(qoi_max_raster))
        else:
            return np.rot90(np.transpose(qoi_max_raster))


    def extract_qoi_max_loc(self, prefix: str, loc: np.ndarray,
        qoi: str) -> np.ndarray:
        """
        Extract maximum value(s) of a quantity of interest (qoi) at specific
        location(s).
        
        Parameters
        ----------
        prefix : str
            Prefix used to name output files.
        loc : 2d numpy array
            Coordinates of interested locations. Shape (nloc, 2), where `nloc`
            is the number of interested locations.
            loc[:,0] - x coordinates
            loc[:,1] - y coordinates
        qoi : str
            Quantity of interest.
            'h' - maximum flow height, in meters
            'v' - maximum flow velocity, in m/s
            'p' - maximum flow pressure, in Pa
            't' - maximum flow kinetic energy, in J

        Returns
        -------
        qoi_max_loc : numpy array
            Consist of maximum value(s) of qoi at each location. Shape (nloc,).
        """       
        if not (loc.ndim == 2 and loc.shape[1] == 2):
            raise ValueError(
                "loc must be a 2d numpy array with first axis corresponding to"
                " the number of locations and second axis to x and y coords")

        if qoi not in ['h','v','p','t']:
            raise ValueError("qoi must be 'h', 'v', 'p', or 't'")
        
        qoi_max_raster_asc = os.path.join(self.dir_sim, f'{prefix}_results',
            f'{prefix}_ascii', f'{prefix}_{qoi}flow_max.asc')
        
        header = [linecache.getline(qoi_max_raster_asc, i) for i in range(1,6)]
        header_values = [float(h.split()[-1].strip()) for h in header]
        ncols, nrows, xll, yll, cellsize = header_values
        ncols = int(ncols)
        nrows = int(nrows)

        x = np.arange(xll, xll+(cellsize*ncols), cellsize)
        y = np.arange(yll, yll+(cellsize*nrows), cellsize)

        if not all([loc[i,0]>=x[0] and loc[i,0]<=x[-1] and loc[i,1]>=y[0] and \
            loc[i,1]<=y[-1] for i in range(len(loc))]):
            raise ValueError(
                "Coordinates in loc must be within the boundary of topography")

        qoi_max_raster = np.loadtxt(qoi_max_raster_asc, skiprows=6)
        qoi_max_raster = np.rot90(np.transpose(qoi_max_raster))

        f_qoi_max = interp2d(x, y, qoi_max_raster)

        qoi_max_loc = [float(f_qoi_max(loc[i,0], loc[i,1])) \
            for i in range(len(loc))]

        return np.array(qoi_max_loc)