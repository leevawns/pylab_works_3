"""Compute optimized spacing for major and minor ticks,
returning a tuple comprising the major tick spacing (float),
the recommended number of significant figures (int) to label the
tick mark, and the number of minor ticks per major (int)."""
import math

_OPTIMAL_SPACING = 72    # pixels

class tickopt(object):
    def __init__(self,xmin,xmax,pixels):
        """Initializes an object with the specified (xmin, xmax) giving the range of the
        axis, and pixels is an integer giving the on-screen range of the scale."""
        self.__xmax = xmax
        self.__xmin = xmin
        self.__range = xmax - xmin
        self.__pixels = pixels
        if self.__range == 0.0:
            self.__range = 1.0e-20
        self.__spacing = self.__span_orderofmagnitude()
        self.sigfigs = self.__sigfigs()
        self.major_spacing,self.minors_per_major = self.__tickspacings()

    def __span_orderofmagnitude(self):
        """Returns the order of magnitude spanned by the data."""
        return math.floor(math.log10(self.__range))

    def __sigfigs(self):
        """Returns the appropriate significant figures for tick labels, given
        the order of magnitude tick spacing."""
        if self.__spacing == 0.0:
            return 1
        elif self.__spacing < 0.0:
            return 1 - int(self.__spacing)
        else:
            return 0

    def __tickspacings(self):
        """Returns a pair containing the major tick spacing (float) and the number of minor ticks per major (int)."""
        major = 10 ** self.__spacing
        maj_spacing = int(major * self.__pixels / self.__range)
        if maj_spacing < (_OPTIMAL_SPACING/5):
            return major * 5.0,5
        elif maj_spacing < (_OPTIMAL_SPACING/2):
            return major * 2.0,2
        elif maj_spacing > (_OPTIMAL_SPACING*2):
            return major * 0.5,5
        return major,5

    def __pixelpos(self,tickval):
        """Returns the pixel position for a given value."""
        return int((tickval - self.__xmin) * self.__pixels / self.__range + 0.5)

    def iter_majors(self):
        """An iterator over the major tick positions.  Successive values are pairs.
        The first element is a string suitable for labelling the tick mark,
        and the second element is the pixel position of the tick mark."""
        fstr = "%%.%df" % self.sigfigs
        major = math.floor(self.__xmin / self.major_spacing) * self.major_spacing
        ppos = self.__pixelpos(major)
        while ppos <= self.__pixels:
            if ppos >= 0:
                yield fstr % major,ppos
            major += self.major_spacing
            ppos = max(self.__pixelpos(major),ppos+1)

    def iter_minors(self):
        """An iterator over minor tick positions.  Each returned value is
        the pixel position of the next minor tick."""
        major = math.floor(self.__xmin / self.major_spacing) * self.major_spacing
        while major <= self.__xmax:
            for n in range(1,self.minors_per_major):
                value = major + (float(n)/self.minors_per_major) * self.major_spacing
                ppos = self.__pixelpos(value)
                if 0 <= ppos <= self.__pixels:
                    yield ppos
            major += self.major_spacing

