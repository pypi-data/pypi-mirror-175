import os
import math
import linecache
import numpy as np
from scipy.integrate import ode
from scipy.interpolate import interp2d
from typing import Union
from beartype import beartype

class MassPointModel:
    """Mass point model."""
    
    @staticmethod
    def _preprocess(elevation, x0, y0):
        """
        Preprocess input data.

        Parameters
        ----------
        elevation : str
            Name of the elevation raster file, in ESRI ascii format, including
            the path.
        x0 : float or int
            x coordinate of initial position.
        y0 : float or int
            y coordinate of initial position.

        Returns
        -------
        fgrad_x : Callable
            Call with `fgrad_x(x, y)`. Return first order partial derivative
            of `elevation` with respect to `x` at location (x, y).
        fgrad_y : callable
            Call with `fgrad_y(x, y)`. Return first order partial derivative
            of `elevation` with respect to `y` at location (x, y).
        fgrad_xx : Callable
            Call with `fgrad_xx(x, y)`. Return second order partial derivative
            of `elevation` with respect to `x` at location (x, y).
        fgrad_yy : Callable
            Call with `fgrad_yy(x, y)`. Return second order partial derivative
            of `elevation` with respect to `y` at location (x, y).
        fgrad_xy : Callable
            Call with `fgrad_xy(x ,y)`. Return second order partial derivative
            of `elevation` with respect to `x` and `y` at location (x, y).
        
        """        
        if not os.path.exists(elevation):
            raise ValueError(f"{elevation} does not exist")

        header = [linecache.getline(elevation, i) for i in range(1,6)]
        header_values = [float(h.split()[-1].strip()) for h in header]
        ncols, nrows, xll, yll, cellsize = header_values
        ncols = int(ncols)
        nrows = int(nrows)

        x_values = np.arange(xll, xll+(cellsize*ncols), cellsize)
        y_values = np.arange(yll, yll+(cellsize*nrows), cellsize)

        if not all([x0>x_values[0], x0<x_values[-1], y0>y_values[0],
            y0<y_values[-1]]):
            raise ValueError(
                "x0 and y0 must be within the boundary of elevation")
        
        z_values = np.loadtxt(elevation, skiprows=6)
        z_values = np.rot90(np.transpose(z_values))
        
        dzdx = np.gradient(z_values, x_values, axis=1)
        dzdy = np.gradient(z_values, y_values, axis=0)
        
        dzdxx = np.gradient(dzdx, x_values, axis=1)
        dzdyy = np.gradient(dzdy, y_values, axis=0)
        dzdxy = np.gradient(dzdx, y_values, axis=0)
        
        fgrad_x = interp2d(x_values, y_values, dzdx)
        fgrad_y = interp2d(x_values, y_values, dzdy)
        fgrad_xx = interp2d(x_values, y_values, dzdxx)
        fgrad_yy = interp2d(x_values, y_values, dzdyy)
        fgrad_xy = interp2d(x_values, y_values, dzdxy)

        return fgrad_x, fgrad_y, fgrad_xx, fgrad_yy, fgrad_xy

    
    @staticmethod
    def _mass_point_model(
        t, alpha, coulomb_friction, turbulent_friction, fgrad_x, fgrad_y,
        fgrad_xx, fgrad_yy, fgrad_xy, g, curvature):
        """
        Define mass point model (3d) which serves as the callable function
        `f(t,alpha,*f_args)` in `scipy.integrate.ode(f)`.

        Parameters:
        -----------
        t : float or int
            Time in seconds.
        alpha : list
            Contains x, y, ux, uy at time t, i.e., [x(t), y(t), ux(t), uy(t)].
        coulomb_friction : float
            Dry Coulomb friction coefficient.
        turbulent_friction : float or int
            Turbulent friction coefficient, in m/s^2.
        fgrad_x : Callable
            Call with `fgrad_x(x, y)`. Return first order partial derivative
            of `elevation` with respect to `x` at location (x, y).
        fgrad_y : Callable
            Call with `fgrad_y(x, y)`. Return first order partial derivative
            of `elevation` with respect to `y` at location (x, y).
        fgrad_xx : Callable
            Call with `fgrad_xx(x, y)`. Return second order partial derivative
            of `elevation` with respect to `x` at location (x, y).
        fgrad_yy : Callable
            Call with `fgrad_yy(x, y)`. Return second order partial derivative
            of `elevation` with respect to `y` at location (x, y).
        fgrad_xy : Callable
            Call with `fgrad_xy(x ,y)`. Return second order partial derivative
            of `elevation` with respect to `x` and `y` at location (x, y).
        g : float or int
            Gravity acceleration, in m/s^2.
        curvature : bool
            Whether to account for the curvature effect.
        
        Return:
        -------
        dalphadt : numpy array 
            Right hand side of the mass point model.

        """
        x, y, ux, uy = alpha[0], alpha[1], alpha[2], alpha[3]

        gradx, grady, gradxx, gradyy, gradxy = fgrad_x(x,y), fgrad_y(x,y), \
            fgrad_xx(x,y), fgrad_yy(x,y), fgrad_xy(x,y)

        sqrt_x = math.sqrt(1 + gradx**2)
        sqrt_y = math.sqrt(1 + grady**2)
        sqrt_xy = math.sqrt(1 + gradx**2 + grady**2)

        gx = gradx * (-g) / sqrt_x
        gy = grady * (-g) / sqrt_y
        gn = g / sqrt_xy

        if curvature:
            kx = gradxx / (1 + gradx**2) / sqrt_xy
            kxy = gradxy / sqrt_x / sqrt_y / sqrt_xy
            ky = gradyy / (1 + grady**2) / sqrt_xy
            uku = kx*ux**2 + 2*kxy*ux*uy + ky*uy**2
        else:
            uku = 0
        
        u = math.sqrt(ux**2 + uy**2 + 2*ux*uy*gradx*grady/sqrt_x/sqrt_y)
        
        dalphadt = np.zeros(len(alpha))

        dalphadt[0] = ux / sqrt_x
        dalphadt[1] = uy / sqrt_y

        if u != 0:
            friction = coulomb_friction*(gn+uku) + g*u**2/turbulent_friction
            dalphadt[2] = gx - (ux/u)*friction
            dalphadt[3] = gy - (uy/u)*friction
        else:
            friction = coulomb_friction*gn
            dalphadt[2] = gx + friction*gradx*(1+gradx**2+grady**2)/sqrt_x/   \
                math.sqrt(gradx**2+grady**2+(gradx**2+grady**2)**2)
            dalphadt[3] = gy + friction*grady*(1+gradx**2+grady**2)/sqrt_y/   \
                math.sqrt(gradx**2+grady**2+(gradx**2+grady**2)**2)

        return dalphadt

    @beartype
    def run(
        self, elevation: str, coulomb_friction: float,
        turbulent_friction: Union[float, int], x0: Union[float, int],
        y0: Union[float, int], ux0: Union[float, int] = 0,
        uy0: Union[float, int] = 0, dt: Union[float, int] = 1,
        tend: Union[float, int] = 300, t0: Union[float, int] = 0,
        g: Union[float, int] = 9.8, atol: float = 1e-6, rtol: float = 1e-6,
        curvature: bool = False) -> np.ndarray:
        """
        Solve the mass point model using scipy.integrate.ode solver given
        required input data.

        Parameters
        ----------
        elevation : str
            Name of the elevation raster file, in ESRI ascii format, including
            the path.
        coulomb_friction : float
            Dry Coulomb friction coefficient.
        turbulent_friction : float or int
            Turbulent friction coefficient, in m/s^2.
        x0 : float or int
            x coordinate of initial position.
        y0 : float or int
            y coordinate of initial position.
        ux0 : float or int
            Initial velocity in x direction.
        uy0 : float or int
            Initial velocity in y direction.
        dt : float or int
            Time step in seconds.
        tend : float or int
            End time in seconds.
        t0 : float or int
            Initial time.
        g : float or int
            Gravity acceleration, in m/s^2.
        atol : float
            Absolute tolerance for solution.
        rtol : float
            Relative tolerance for solution.
        curvature : bool
            Whether to account for the curvature effect.
        
        Returns
        -------
        output: numpy array, 2d
        Time history of the mass point's location and velocity.
        output[:,0] - time
        output[:,1] - x coordinate
        output[:,2] - y coordinate
        output[:,3] - velocity in x direction
        output[:,4] - velocity in y direction
        output[:,5] - total velocity
        
        """
        fgrad_x, fgrad_y, fgrad_xx, fgrad_yy, fgrad_xy = \
            self._preprocess(elevation, x0, y0)
        
        s = ode(self._mass_point_model).set_integrator('dopri5', method='bdf',
            atol=atol, rtol=rtol)
        
        s.set_f_params(coulomb_friction, turbulent_friction, fgrad_x, fgrad_y,
            fgrad_xx,fgrad_yy,fgrad_xy, g, curvature)
        
        alpha0 = [x0, y0, ux0, uy0]
        s.set_initial_value(alpha0, t0)

        t_all = [t0]
        alpha_all = [alpha0]

        while s.successful() and s.t < tend:
            s.integrate(s.t + dt)
            t_all.append(s.t)
            alpha_all.append(s.y)
        
        t_all = np.array(t_all)
        alpha_all = np.array(alpha_all)

        u = np.zeros(len(t_all))
        for i in range(len(t_all)):
            gradx = fgrad_x(alpha_all[i,0], alpha_all[i,1])
            grady = fgrad_y(alpha_all[i,0], alpha_all[i,1])
            ux = alpha_all[i,2]
            uy = alpha_all[i,3]
            u[i] = math.sqrt(ux**2 + uy**2 + 2*ux*uy*gradx*grady/
                math.sqrt(1+gradx**2)/math.sqrt(1+grady**2))
            
        t_all = np.reshape(t_all,(len(t_all),-1))
        u = np.reshape(u,(len(u),-1))
        output = np.concatenate((t_all, alpha_all, u), axis=1)
        
        return output