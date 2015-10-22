namespace util
{
  double mtt(double mll, double l0pt, double l0phi, double l1pt, double l1phi, double met, double metphi)
  {
    double l0x = l0pt*cos(l0phi);
    double l0y = l0pt*sin(l0phi);
    
    double l1x = l1pt*cos(l1phi);
    double l1y = l1pt*sin(l1phi);
    
    double metx = met*cos(metphi);
    double mety = met*sin(metphi);  
    
    double x_1= (l0x*l1y-l0y*l1x)/(l1y*metx-l1x*mety+l0x*l1y-l0y*l1x);
    double x_2= (l0x*l1y-l0y*l1x)/(l0x*mety-l0y*metx+l0x*l1y-l0y*l1x);
    
    if(x_1 > 0 && x_2 > 0)
      return mll/sqrt(x_1*x_2);
    else 
      return -9.999;
  }
}
