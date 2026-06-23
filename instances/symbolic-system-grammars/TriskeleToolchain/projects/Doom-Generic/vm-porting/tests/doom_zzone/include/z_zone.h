//


//




//




//


//	Remark: this was the only stuff that, according
//	 to John Carmack, might have been useful for
//	 Quake.
//



#ifndef __Z_ZONE__
#define __Z_ZONE__

#include "z_zone_stubs.h"

//



enum
{
    PU_STATIC = 1,                  
    PU_SOUND,                       
    PU_MUSIC,                       
    PU_FREE,                        
    PU_LEVEL,                       
    PU_LEVSPEC,                     
    
    

    PU_PURGELEVEL,
    PU_CACHE,

    

    PU_NUM_TAGS
};
        

void	Z_Init (void);
void*	Z_Malloc (int size, int tag, void *ptr);
void    Z_Free (void *ptr);
void    Z_FreeTags (int lowtag, int hightag);
void    Z_DumpHeap (int lowtag, int hightag);
void    Z_FileDumpHeap (FILE *f);
void    Z_CheckHeap (void);
void    Z_ChangeTag2 (void *ptr, int tag, char *file, int line);
void    Z_ChangeUser(void *ptr, void **user);
int     Z_FreeMemory (void);
unsigned int Z_ZoneSize(void);

//


//
#define Z_ChangeTag(p,t)                                       \
    Z_ChangeTag2((p), (t), __FILE__, __LINE__)


#endif
