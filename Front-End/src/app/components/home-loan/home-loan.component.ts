import { Component, OnInit } from '@angular/core';
import { HomeLoanService } from 'src/app/services/home-loan.service';
import { AuthenticationService } from 'src/app/services/authentication.service'; // Import the AuthenticationService
import * as alertify from 'alertifyjs';
import { catchError } from 'rxjs/operators';
import { of, throwError } from 'rxjs';
import { HomeLoan } from 'src/app/model/home-loan';

@Component({
  selector: 'app-home-loan',
  templateUrl: './home-loan.component.html',
  styleUrls: ['./home-loan.component.css']
})
export class HomeLoanComponent implements OnInit { // Implement OnInit interface
  principal!: number;
  homeLoanData: HomeLoan = { principal: 0, interestRate: 0, loanTerm: 0 };
  homeLoanResult: any;
  interestRate!: number;
  loanTerm!: number;
  username: string = '';

  constructor(
    private homeLoanService: HomeLoanService,
    private authService: AuthenticationService // Inject AuthenticationService
  ) { }

  ngOnInit() {
    // Retrieve the authenticated user's data, including the username
    const authenticatedUser = this.authService.getAuthenticatedUser();
    if (authenticatedUser) {
      this.username = authenticatedUser.username;
    }
  }

  calculateHomeLoan() {
    if (this.username) {
      const homeLoanData: HomeLoan = {
        principal: this.principal,
        interestRate: this.interestRate,
        loanTerm: this.loanTerm
      };

      this.homeLoanService
        .calculateHomeLoan(this.homeLoanData, this.username)
        .pipe(
          catchError((error) => {
            alertify.error('Failed to calculate Home Loan.');
            return throwError('Failed to calculate Home Loan.');
          })
        )
        .subscribe((result) => {
          console.log(' Home Loan Result:', result); // Log the result
          if (result) {
            this.homeLoanResult = result;
            alertify.success('Home Loan calculated successfully.');
          }
        });
    }
  }
}
