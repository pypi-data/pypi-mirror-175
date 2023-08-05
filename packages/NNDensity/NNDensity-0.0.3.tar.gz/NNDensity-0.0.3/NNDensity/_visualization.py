'''
Visualization Tools
-----------------
'''

import matplotlib.pyplot as plt
import numpy as np
from ._NNDE import AWNN,TKNN,BKNN,KNN,WKNN,AKNN
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import patches

method_dict={
    "AWNN":AWNN,
    "TKNN":TKNN,
    "BKNN":BKNN,
    "KNN":KNN,
    "WKNN":WKNN,
    "AKNN":AKNN
    }



class contour3d(object):
    """contour3d
        Parameters
        ----------
        data : numpy.ndarray
            data used for plotting
        grid_x : string or numpy.ndarry, default = "auto"
            grids on x axis
        grid_y : string or numpy.ndarry, default = "auto"
            grids on y axis
        method : string default = "AWNN"
            method used to train model
        figsize : turple
            The size of figure
        xlim : string default = "auto"
            The maximum and minimum of x-axis
        ylim : string default = "auto"
            The maximum and minimum of y-axis
        zlim : string default = "auto"
            The maximum and minimum of z-axis
        color_scheme : string
            The cmap plot functions use
        elev : float default = 20
            elevation of 3d plot
        azim : float default = 75
            azimuth of 3d plot
        alpha : float default = 1
            The transparency of the image
        Attributes
        ----------
        estimation : numpy.ndarray
            estimation of model
        """
    def __init__(
        self,
        data,
        grid_x = "auto",
        grid_y = "auto",
        method = "AWNN",
        figsize = (7,5),
        xlim = "auto",
        ylim = "auto",
        zlim = "auto",
        color_scheme = "rainbow",
        elev = 20,
        azim = 75,
        alpha = 1,
        **kargs,
    ):
        assert type(data) is np.ndarray
        assert data.shape[1] == 2
        self.data = data
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.xlim = xlim
        self.ylim = ylim
        if self.xlim == "auto":
            if self.grid_x == "auto":
                self.xlim = (self.data[:,0].min(),self.data[:,0].max())
            else:
                self.xlim = (min(self.grid_x),max(self.grid_x))
        if self.ylim == "auto":
            if self.grid_y == "auto":
                self.ylim = (self.data[:,1].min(),self.data[:,1].max())
            else:
                self.xlim = (min(self.grid_y),max(self.grid_y))
        if self.grid_x == "auto":
            self.grid_x = np.linspace(self.xlim[0],self.xlim[1],30)
        if self.grid_y == "auto":
            self.grid_y = np.linspace(self.ylim[0],self.ylim[1],30)
        self.kargs = kargs
        self.method=method
        self.figsize = figsize
        self.zlim = zlim
        self.color_scheme = color_scheme
        self.elev = elev
        self.azim = azim
        self.alpha = alpha
        
    def estimation(self):
        """ do estimation"""
        axis0,axis1 = np.meshgrid(self.grid_x,self.grid_y)
        X_grid = np.array([axis0.ravel(),axis1.ravel()]).T
        #print(self.data)
        model = method_dict[self.method](**self.kargs).fit(self.data)
        self.estimation = np.exp(model.predict(X_grid)).reshape(-1,len(self.grid_y))
        if self.zlim == "auto":
            self.zlim = (0,self.estimation.max())

    def make_plot(self):
        """generate screen
            Returns
            -------
            fig : matplotlib.figure.Figure
            """
        fig = plt.figure(figsize=self.figsize)
        ax = fig.add_subplot(111,projection="3d")
        axis0, axis1 = np.meshgrid(self.grid_x,self.grid_y)
        ax.plot_surface(axis0, axis1, self.estimation, cmap = plt.get_cmap(self.color_scheme),alpha = self.alpha)
        ax.set_xlim(self.xlim[0],self.xlim[1])
        ax.set_ylim(self.ylim[0],self.ylim[1])
        ax.set_zlim(self.zlim[0],self.zlim[1])
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.02f')) 
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.02f')) 
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        ax.xaxis.set_major_locator(LinearLocator(4)) 
        ax.yaxis.set_major_locator(LinearLocator(4)) 
        ax.zaxis.set_major_locator(LinearLocator(4))
        plt.xlabel("x")
        plt.ylabel("y")
        ax.view_init(elev = self.elev,azim = self.azim)
        return fig
    
    def plot(self):
        """ do plot """
        self.estimation()
        return self.make_plot()
    
        

class lineplot(object):
    """lineplot
        Parameters
        ----------
        data : numpy.ndarray
            data used for plotting
        method_seq : list default = ["AWNN"]
            methods used to train model
        figsize : turple
            The size of figure
        x_start : string or numpy.ndarray default = "auto"
            start point of slicing line, if default, it is the 
            minimum of each dimension
        x_end : string or numpy.ndarray default = "auto"
            end point of slicing line, if default, it is the 
            maximum of each dimension
        num_grid : int default = 100
            the number of grids
        alpha : float default = 1
            The transparency of the image
        true_density_obj : object default = None
            the density generation object defined in NNDE used to generate data
        """
    def __init__(
            self,
            data,
            method_seq = ["AWNN"],
            figsize = (7,5),
            x_start = "auto",
            x_end = "auto",
            num_grid = 100,
            alpha = 1,
            true_density_obj = None,
            kargs_seq = None,
            ):
        assert type(data) is np.ndarray
        self.data = data
        self.method_seq = method_seq
        self.figsize = figsize
        self.num_grid = num_grid
        if x_start == "auto":
            self.x_start = np.array([self.data[:,i].min() for i in range(self.data.shape[1])])
        if x_end == "auto":
            self.x_end = np.array([self.data[:,i].max() for i in range(self.data.shape[1])])
        self.test_grid = np.hstack([np.linspace(self.x_start[i],self.x_end[i],self.num_grid).reshape(-1,1)
                                  for i in range(self.data.shape[1])])
        self.lamda_seq = np.linspace(0, 1,self.num_grid)
        self.alpha = alpha
        self.kargs_seq = kargs_seq
        if self.kargs_seq is None:
            self.kargs_seq= [ {} for method in self.method_seq]
        
        self.ylim = [0,0]
        self.true_density_obj = true_density_obj
        if self.true_density_obj:
            self.test_pdf = true_density_obj.density(self.test_grid)

    def plot(self):
        """generate screen
            Returns
            -------
            fig : matplotlib.figure.Figure
            """
        # generate screen
        fig, ax = plt.subplots()
        for method_idx, method in enumerate( self.method_seq) :
            model = method_dict[method](**self.kargs_seq[method_idx]).fit(self.data)
            estimation = np.exp(model.predict(self.test_grid))
            self.ylim[1] = max(self.ylim[1], estimation.max())*1.05 
            line,  = ax.plot(self.lamda_seq, estimation.ravel(),linestyle = '-',label = method)
        if self.true_density_obj:
            line,  = ax.plot(self.lamda_seq,self.test_pdf,linestyle = '-',label = "f(x)")
        ax.set_xlabel(r'$\lambda$',fontsize = 12)
        ax.set_ylabel("Density",fontsize = 12)
        ax.set_xlim([0,1])
        ax.set_ylim(self.ylim)
        ax.legend()
        rectangle = patches.Rectangle((0, self.ylim[0]), 1,self.ylim[1]-self.ylim[0],facecolor = "grey",alpha = 0.2)
        _ = ax.add_patch(rectangle)
        return fig
        
        

class contourf2d(object):
    """contourf2d
        Parameters
        ----------
        data : numpy.ndarray
            data used for plotting
        grid_x : string or numpy.ndarry, default = "auto"
            grids on x axis
        grid_y : string or numpy.ndarry, default = "auto"
            grids on y axis
        method : string default = "AWNN"
            method used to train model
        figsize : turple
            The size of figure
        xlim : string default = "auto"
            The maximum and minimum of x-axis
        ylim : string default = "auto"
            The maximum and minimum of y-axis
        color_scheme : string
            The cmap plot function use
        alpha : float default = 1
            The transparency of the image
        Attributes
        ----------
        estimation : numpy.ndarray
            estimation of model
        """
    def __init__(
        self,
        data,
        grid_x = "auto",
        grid_y = "auto",
        method = "AWNN",
        figsize = (7,5),
        xlim = "auto",
        ylim = "auto",
        color_scheme = "rainbow",
        alpha = 1,
        **kargs,
    ):
        assert type(data) is np.ndarray
        assert data.shape[1] == 2
        self.data = data
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.xlim = xlim
        self.ylim = ylim
        if self.xlim == "auto":
            if self.grid_x == "auto":
                self.xlim = (self.data[:,0].min(),self.data[:,0].max())
            else:
                self.xlim = (min(self.grid_x),max(self.grid_x))
        if self.ylim == "auto":
            if self.grid_y == "auto":
                self.ylim = (self.data[:,1].min(),self.data[:,1].max())
            else:
                self.xlim = (min(self.grid_y),max(self.grid_y))
        if self.grid_x == "auto":
            self.grid_x=np.linspace(self.xlim[0],self.xlim[1],30)
        if self.grid_y == "auto":
            self.grid_y = np.linspace(self.ylim[0],self.ylim[1],30)
        self.kargs = kargs
        self.method = method
        self.figsize = figsize
        self.color_scheme = color_scheme
        self.alpha = alpha
        
    def estimation(self):
        """ do estimation"""
        axis0,axis1 = np.meshgrid(self.grid_x,self.grid_y)
        X_grid = np.array([axis0.ravel(),axis1.ravel()]).T
        #print(self.data)
        model = method_dict[self.method](**self.kargs).fit(self.data)
        self.estimation = np.exp(model.predict(X_grid)).reshape(-1,len(self.grid_y))

    def make_plot(self):
        """generate screen
            Returns
            -------
            fig : matplotlib.figure.Figure
            
            """
        fig = plt.figure(figsize = self.figsize)
        axis0, axis1 = np.meshgrid(self.grid_x,self.grid_y)
        plt.contour(axis0, axis1, self.estimation, cmap = plt.get_cmap(self.color_scheme),alpha = self.alpha)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.colorbar()
        return fig
    
    def plot(self):
        """ do plot """
        self.estimation()
        return self.make_plot()
    


class contour2d(object):
    """contour2d
        Parameters
        ----------
        data : numpy.ndarray
            data used for plotting
        grid_x : string or numpy.ndarry, default = "auto"
            grids on x axis
        grid_y : string or numpy.ndarry, default = "auto"
            grids on y axis
        method : string default = "AWNN"
            method used to train model
        figsize : turple
            The size of figure
        xlim : string default = "auto"
            The maximum and minimum of x-axis
        ylim : string default = "auto"
            The maximum and minimum of y-axis
        color_scheme : string
            The cmap plot function use
        alpha : float default = 1
            The transparency of the image
        Attributes
        ----------
        estimation : numpy.ndarray
            estimation of model
        """
    def __init__(
        self,
        data,
        grid_x = "auto",
        grid_y = "auto",
        method = "AWNN",
        figsize = (7,5),
        xlim = "auto",
        ylim = "auto",
        color_scheme = "rainbow",
        alpha = 1,
        **kargs,
    ):
        assert type(data) is np.ndarray
        assert data.shape[1] == 2
        self.data = data
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.xlim = xlim
        self.ylim = ylim
        if self.xlim == "auto":
            if self.grid_x == "auto":
                self.xlim = (self.data[:,0].min(),self.data[:,0].max())
            else:
                self.xlim = (min(self.grid_x),max(self.grid_x))
        if self.ylim == "auto":
            if self.grid_y == "auto":
                self.ylim = (self.data[:,1].min(),self.data[:,1].max())
            else:
                self.xlim = (min(self.grid_y),max(self.grid_y))
        if self.grid_x == "auto":
            self.grid_x = np.linspace(self.xlim[0],self.xlim[1],30)
        if self.grid_y == "auto":
            self.grid_y = np.linspace(self.ylim[0],self.ylim[1],30)
        self.kargs = kargs
        self.method = method
        self.figsize = figsize
        self.color_scheme = color_scheme
        self.alpha = alpha
        
    def estimation(self):
        """ do estimation"""
        axis0,axis1 = np.meshgrid(self.grid_x,self.grid_y)
        X_grid = np.array([axis0.ravel(),axis1.ravel()]).T
        #print(self.data)
        model = method_dict[self.method](**self.kargs).fit(self.data)
        self.estimation = np.exp(model.predict(X_grid)).reshape(-1,len(self.grid_y))

    def make_plot(self):
        """generate screen
            Returns
            -------
            fig : matplotlib.figure.Figure
            """
        fig = plt.figure(figsize=self.figsize)
        axis0, axis1 = np.meshgrid(self.grid_x,self.grid_y)
        plt.contourf(axis0, axis1, self.estimation, cmap = plt.get_cmap(self.color_scheme),alpha = self.alpha)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.colorbar()
        return fig
    
    def plot(self):
        """ do plot """
        self.estimation()
        return self.make_plot()
        