void checktree(const char* file, const char* brname="") { 
  TFile* f = TFile::Open(file,"read"); if( !f || f->IsZombie() ) { std::cout << "ERROR" << std::endl; return; } 
  TTree* t = (TTree*)f->Get("MVA");    if( !t )                  { std::cout << "ERROR" << std::endl; return; } 
  if( brname != "" ) 
  {
    TBranch* b = t->GetBranch(brname); 
    if( !b )                                                     { std::cout << "ERROR" << std::endl;  return; } 
  }
}
