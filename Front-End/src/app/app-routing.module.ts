import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { HomeLoanComponent } from './components/home-loan/home-loan.component';
import { InvestmentCalculatorComponent } from './components/investment-calculator/investment-calculator.component';
import { SideBarNavComponent } from './components/side-bar-nav/side-bar-nav.component';

const routes: Routes = [
  {path: 'login', pathMatch: 'full', component: LoginComponent},
  {path: 'home', pathMatch: 'full', component: HomeComponent},
  {path: 'home-loan', pathMatch: 'full', component: HomeLoanComponent},
  {path: 'investment', pathMatch: 'full', component: InvestmentCalculatorComponent},
  {path: 'side-bar-nav', pathMatch: 'full', component: SideBarNavComponent},
 
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
