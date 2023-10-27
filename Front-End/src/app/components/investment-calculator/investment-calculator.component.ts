import { Component, OnInit } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { Investment } from 'src/app/model/investment';
import { InvestmentService } from 'src/app/services/investment.service';
import * as alertify from 'alertifyjs';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-investment-calculator',
  templateUrl: './investment-calculator.component.html',
  styleUrls: ['./investment-calculator.component.css']
})
export class InvestmentCalculatorComponent implements OnInit {
// investment.component.ts
  investmentData: Investment = { investmentAmount: 0, annualInterestRate: 0, years: 0 };
  investmentAmount!: number;
  annualInterestRate!: number;
  investmentResult: any;
  years!: number;
  username: string = '';

  constructor(private investmentService: InvestmentService, 
    private authService: AuthenticationService) {}

    ngOnInit() {
      // Retrieve the authenticated user's data, including the username
      const authenticatedUser = this.authService.getAuthenticatedUser();
      if (authenticatedUser) {
        this.username = authenticatedUser.username;
      }
    }
  

  calculateInvestment() {
    if (this.username) {
      this.investmentService
        .calculateInvestment(this.investmentData, this.username)
        .pipe(
          catchError((error) => {
            alertify.error('Failed to calculate Investment.');
            return throwError('Failed to calculate Investment.');
          })
        )
        .subscribe((result) => {
          console.log('Investment Result:', result); // Log the result
          if (result) {
            this.investmentResult = result;
            alertify.success('Investment calculated successfully.');
          }
        });
    } else {
      alertify.error('Username is not defined.');
    }
  }
}

