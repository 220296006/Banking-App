import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AngularMaterialModule } from './modules/material/material.module';
import { LoginComponent } from './components/login/login.component';
import { LoginService } from './services/login.service';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HomeComponent } from './components/home/home.component';
import { HomeLoanComponent } from './components/home-loan/home-loan.component';
import { InvestmentCalculatorComponent } from './components/investment-calculator/investment-calculator.component';
import { SideBarNavComponent } from './components/side-bar-nav/side-bar-nav.component';
import { MatIconModule } from '@angular/material/icon';
import { CalculationResultComponent } from './components/calculation-result/calculation-result.component';
import { HomeLoanService } from './services/home-loan.service';
import { InvestmentService } from './services/investment.service';
import { AuthenticationService } from './services/authentication.service';
import { AuthInterceptor } from './services/auth-interceptor.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    HomeLoanComponent,
    InvestmentCalculatorComponent,
    SideBarNavComponent,
    CalculationResultComponent,
    ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AngularMaterialModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    MatIconModule
  ],
  
    providers: [LoginService, HomeLoanService, InvestmentService, AuthenticationService, {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }],
  bootstrap: [AppComponent]
})
export class AppModule { }
