import { Component } from '@angular/core';
import { HomeLoanService } from 'src/app/services/home-loan.service';
import * as alertify from 'alertifyjs';
import { catchError } from 'rxjs/operators';
import { of, throwError } from 'rxjs';
import { HomeLoan } from 'src/app/model/home-loan';

@Component({
  selector: 'app-home-loan',
  templateUrl: './home-loan.component.html',
  styleUrls: ['./home-loan.component.css']
})
export class HomeLoanComponent {
  principal!: number;
  homeLoanData: HomeLoan = { principal: 0, interestRate: 0, loanTerm: 0 };
  homeLoanResult: any;
  interestRate!: number;
  loanTerm!: number
  username: string = '';

  constructor(private homeLoanService: HomeLoanService) {}

  calculateHomeLoan() {
    if (this.username) {
      this.homeLoanService
        .calculateHomeLoan(this.homeLoanData)
        .pipe(
          catchError((error) => {
            alertify.error('Failed to calculate Home Loan.');
            return throwError('Failed to calculate Home Loan.');
          })
        )
        .subscribe((result) => {
          if (result) {
            this.homeLoanResult = result;
            alertify.success('Home Loan calculated successfully.');
          }
        });
    } else {
      alertify.error('Username is not defined.');
    }
  }
}
