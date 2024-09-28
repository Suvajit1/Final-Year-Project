#include<stdio.h>
#include"gmp.h"
//#define ORDER_SCALE_DOWN_VAL "68"

void add_point(mpz_t a,mpz_t b,mpz_t p,mpz_t xp,mpz_t yp,mpz_t xq,mpz_t yq,mpz_t xr,mpz_t yr)
{
	mpz_t l,modx,mody,temp1,temp2,temp3,pm,pp;  
	mpz_init(l);mpz_init(temp1);mpz_init(temp2);mpz_init(temp3);mpz_init(modx);mpz_init(mody);mpz_init(pp);mpz_init(pm);
        mpz_set(pp,yq);
	mpz_sub(pm,p,pp);
        if(mpz_cmp_ui(xp,0)==0&&mpz_cmp_ui(yp,0)==0)
         {
             mpz_set(xr,xq);
             mpz_set(yr,yq);
             return;
        }
        
        if(mpz_cmp_ui(yq,0)==0&&mpz_cmp_ui(xq,0)==0)
          {
            mpz_set(xr,xp);
             mpz_set(yr,yp);
             return;       
          }

              
        if(mpz_cmp(xp,xq)==0 && mpz_cmp(yp,pm)==0)
        {

        //	printf("ZERO POINT DETECTED.");
	//	exit(0);
                mpz_set_ui(xr,0);
                mpz_set_ui(yr,0);
                return; 
	}
	mpz_sub(temp1,yq,yp);
	mpz_sub(temp2,xq,xp);
	mpz_mod(mody,temp1,p);
	mpz_invert(modx,temp2,p);
	//gmp_printf("\nmodx is :%Zd,temp2 is %Zd, p is %Zd\n",modx,temp2,p);
	mpz_mul(temp1,modx,mody);
	mpz_mod(l,temp1,p);
 	//	xr=mod(((l*l)-xp-xq),m);
	mpz_pow_ui(temp1,l,2);
	mpz_add(temp2,xp,xq);
	mpz_sub(temp3,temp1,temp2);
	mpz_mod(xr,temp3,p);
    	//	yr=mod((l*(xp-xr)-yp),p);
	mpz_sub(temp1,xp,xr);
	mpz_mul(temp2,temp1,l);
	mpz_sub(temp3,temp2,yp);
	mpz_mod(yr,temp3,p);
	
	/*  Clear all variables  */
	mpz_clear(l); mpz_clear(modx); mpz_clear(mody); mpz_clear(temp1); mpz_clear(temp2); mpz_clear(temp3);mpz_clear(pm);mpz_clear(pp);
    		
}


void double_point(mpz_t a,mpz_t b, mpz_t p,mpz_t xp,mpz_t yp,mpz_t xr,mpz_t yr)
{
	mpz_t l,modx,mody,temp1,temp2,temp3;
	mpz_init(l);mpz_init(temp1);
	mpz_init(temp2);mpz_init(temp3);mpz_init(modx);mpz_init(mody);
   	if(mpz_cmp_ui(yp,0)==0)
	{
		//printf("ZERO POINT DETECTED.");
		//exit(0);
                mpz_set_ui(xr,0);
                mpz_set_ui(yr,0);
                return;
	}
        //l=mod((mod(((3*xp*xp)+a),m)*inversemod((2*yp),m)),m);
        mpz_pow_ui(temp1,xp,2);
	mpz_mul_ui(temp1,temp1,3);
	mpz_add(temp2,temp1,a);
	mpz_mod(modx,temp2,p);				
	mpz_mul_ui(temp1,yp,2);
	mpz_invert(mody,temp1,p);
	mpz_mul(temp3,modx,mody);
	mpz_mod(l,temp3,p);
    	//xr=mod(((l*l)-xp-xq),m);
	mpz_pow_ui(temp1,l,2);
	mpz_mul_ui(temp2,xp,2);
	mpz_sub(temp3,temp1,temp2);
	mpz_mod(xr,temp3,p);

    	//yr=mod((l*(xp-xr)-yp),m);
	mpz_sub(temp1,xp,xr);
	mpz_mul(temp2,temp1,l);
	mpz_sub(temp3,temp2,yp);
	mpz_mod(yr,temp3,p);

	 /*  Clear all variables  */
	mpz_clear(l); mpz_clear(modx); mpz_clear(mody); mpz_clear(temp1); mpz_clear(temp2); mpz_clear(temp3);

}

void find_order(mpz_t a,mpz_t b,mpz_t p,mpz_t xp,mpz_t yp,mpz_t order)
{
        mpz_t l,modx,mody,temp1,temp2,temp3,xq,yq,xr,yr,c;  
        mpz_init(l);mpz_init(temp1);mpz_init(temp2);mpz_init(temp3);mpz_init(modx);
        mpz_init(mody);mpz_init(xq);mpz_init(yq);mpz_init(xr);mpz_init(yr);

        mpz_set(xq,xp);
        mpz_set(yq,yp);
        mpz_init(c);
	mpz_set_ui(c,1);
        double_point(a,b,p,xq,yq,xr,yr);
        if(mpz_cmp_ui(xr,0)==0 && mpz_cmp_ui(yr,0)==0)
        {
          mpz_set_ui(order,2);
          return;
        } 
	mpz_add_ui(c,c,1);
        mpz_set(xq,xr);
        mpz_set(yq,yr);
        while(1)
        {
                mpz_add_ui(c,c,1);
                if(mpz_cmp(xp,xq)==0)
                {
                        mpz_set(order,c);
                        break;
                }
                else
                {
                        add_point(a,b,p,xp,yp,xq,yq,xr,yr);
                        mpz_set(xq,xr);
                        mpz_set(yq,yr);
                }
        }
        // Clear all variables
        mpz_clear(l); mpz_clear(modx); mpz_clear(mody); mpz_clear(temp1); mpz_clear(temp2); mpz_clear(temp3);
        mpz_clear(xq);mpz_clear(yq);mpz_clear(xr);mpz_clear(yr);mpz_clear(c);
        /*
	mpz_t temp1;
        mpz_init(temp1);
        mpz_set_str ( temp1, ORDER_SCALE_DOWN_VAL, 10 );
        mpz_fdiv_q(order,p,temp1);      // Order Scale Down
	mpz_clear(temp1);
        */
}

int main(int argc,char *argv[])
{
        gmp_printf("hello");
	mpz_t xp,yp,order,m,a,b;
        mpz_init(xp);mpz_init(yp);mpz_init(order);mpz_init(m);mpz_init(a);mpz_init(b);
	mpz_set_str(a,argv[1],10);
        mpz_set_str(b,argv[2],10);
        mpz_set_str(m,argv[3],10);
	mpz_set_str(xp,argv[4],10);
        mpz_set_str(yp,argv[5],10);

	
	find_order(a,b,m,xp,yp,order);
	gmp_printf("\nOrder is::%Zd\n",order);

		
	return 0;
}
